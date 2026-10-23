"""Route informal intent to interpretive frames; code alone binds and validates them."""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import itertools
import json
import math
import os
from pathlib import Path
import random
import re
import sys
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'experiments/verified_bridge_relevance'))
import benchmark_relevance as geometry

MODEL = 'jev-1.14.0'
SEED = 2026102308
PARENT = '6854789f4bf92974b9411c6a41c8340c82be9ea2'
FRAMES = {
    'triangles': {
        'title': 'Confronto fra due triangoli sul carrier comune',
        'description': 'Confrontare due parti triangolari adiacenti organizzandole attorno al segmento materiale che condividono. Non richiede uguaglianza di forma o dimensioni.',
        'source_kind': 'historical_local_contract',
        'source': 'GS_HIST_DOUBLE_TRIANGLE',
    },
    'polyrole': {
        'title': 'Identità dello stesso carrier in ruoli diversi',
        'description': 'Seguire lo stesso oggetto materiale nei diversi impieghi: bordo di ciascuna regione e separazione interna della figura intera. Il tema è la relazione fra parte, tutto e identità del carrier.',
        'source_kind': 'historical_local_contract',
        'source': 'GS_HIST_MEDIAL_POLYROLE',
    },
    'congruence': {
        'title': 'Corrispondenza di forma e dimensioni',
        'description': 'Cercare due regioni congruenti: sovrapponibili con traslazioni, rotazioni o riflessioni, senza deformazioni o cambi di scala. La sola adiacenza non basta.',
        'source_kind': 'previous_grammar_proposal_not_historical_GS',
        'source': 'NEW_CONGRUENT_PAIR',
    },
}
# These annotations are proposed by the benchmark author before the call, not
# independent human judgments and not consequences of a geometric predicate.
CASES = [
    {'id': 'paired_parts', 'text': 'Voglio mettere a confronto due pezzi triangolari adiacenti usando il tratto che hanno in comune, senza chiedere che siano uguali.',
     'acceptable': [['triangles']], 'reason': 'Focus on organizing adjacent triangular parts, not tracking the part/whole roles.'},
    {'id': 'object_identity', 'text': 'Mi interessa seguire lo stesso oggetto quando fa da bordo di ciascuna parte e contemporaneamente da separazione dell’intera figura.',
     'acceptable': [['polyrole']], 'reason': 'Focus on the material identity across boundary and partition roles.'},
    {'id': 'two_perspectives', 'text': 'Vorrei sia leggere insieme le due parti triangolari sul tratto comune, sia seguire i diversi impieghi di quello stesso tratto nel tutto.',
     'acceptable': [['polyrole', 'triangles']], 'reason': 'Both perspectives explicitly requested; do not force a single frame.'},
    {'id': 'unavailable_but_relevant', 'text': 'Cerchiamo due parti sovrapponibili senza deformazioni, anche capovolgendone una. Vorrei confrontarne forma e dimensioni.',
     'acceptable': [['congruence']], 'reason': 'Semantic relevance survives a later failure to instantiate congruence in this finite construction catalog.'},
    {'id': 'out_of_catalog', 'text': 'Calcolami l’area del triangolo e dammi un numero.',
     'acceptable': [[]], 'reason': 'A numerical area computation is outside all three supplied interpretive frames; none is not geometric impossibility.'},
    {'id': 'underspecified', 'text': 'Vorrei capire meglio questa figura, ma non so ancora cosa confrontare.',
     'acceptable': ['clarify', ['congruence', 'polyrole', 'triangles']],
     'reason': 'Clarify the intent or keep all perspectives open. No unique reference; probability splitting alone is not simultaneous relevance.'},
]
STOP = set('a ad al alla alle anche attorno che chi con da dal dalla dei del della delle di e ed fra gli i il in la le lo nei nel nella non o per piu quale questo se sia solo su sul sulla tra un una uno'.split())
LIMITS = [
    'One paid call, six native Choice questions. Each option is a SET of frames, including all subsets, none, and clarification. No Score, composite, repair calls or retries.',
    'Jev sees informal Italian intents and a semantic catalog, not bridge IDs, coordinates, bindings, geometric availability or author annotations. Text only intentionally isolates routing; images have not been tested here.',
    'Two frames refer to historical LOCAL contracts; congruence is an existing grammar proposal, not another historical GS. The catalog is three perspectives, not a Euclid corpus.',
    'The same workspace is used for all six intents. Code executes only selected perspectives over three fixed prospective cuts. It checks historical local contracts and triangle SSS numerically; no new open-ended construction or formal theorem proof.',
    'Author-authored synthetic intents and predeclared acceptable sets are a smoke test, not independent human validation, held-out paraphrase generalization or universal relevance truth.',
    'The ambiguous intent has two acceptable actions (clarify or retain all). Multiple useful perspectives are encoded as a set option rather than selecting a winner from mutually exclusive single frames.',
    'Baselines are a frozen exact-token-overlap heuristic and explore-all. Dispatch/check counts are deterministic work units, not measured latency, monetary savings or proof-search performance. Baselines make no paid calls.',
    'A selected relevant frame can have no certified binding in the finite cut catalog. Report that separately from semantic routing errors. Code never manufactures a binding from a model choice.',
    'All intents share one state/request and are correlated. No causal comparison with prior geometry tests, calibrated probabilities, autonomous discovery, visual comprehension or internal sequential reasoning is established.',
    'Native probabilities/confidence/usage are retained; absent reliability is null. No confidence gate or threshold tuned after observing answers. Clarification/none are explicit returned options.',
]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def tokens(text):
    plain = ''.join(c for c in unicodedata.normalize('NFKD', text.lower()) if not unicodedata.combining(c))
    return set(re.findall(r'[a-z]+', plain)) - STOP


def lexical(text):
    words = tokens(text)
    counts = {k: len(words & tokens(v['title'] + ' ' + v['description'])) for k, v in FRAMES.items()}
    top = max(counts.values())
    return sorted(k for k, n in counts.items() if n == top) if top else []


def decision_key(action):
    return 'clarify' if action == 'clarify' else '+'.join(sorted(action)) or 'none'


def make_fixture():
    rng = random.Random(SEED)
    frames = list(FRAMES)
    rng.shuffle(frames)
    aliases = dict(zip(frames, ['F' + str(n) for n in rng.sample(range(100, 999), 3)]))
    state = {
        'workspace': {'scope': 'One triangular host; prospective subdivisions may be explored by a separate code component.',
                      'mental_space_kinds': ['original host', 'potential subregions', 'material carrier and its participations']},
        'perspectives': {aliases[k]: {'title': FRAMES[k]['title'], 'description': FRAMES[k]['description']} for k in frames},
        'intents': {},
        'policy': 'Interpret each referenced user request independently. Select the smallest set of semantic perspectives covering its explicitly requested interests. Several perspectives may be useful together. Do not decide geometric feasibility: another component binds objects and checks constraints. For an unsupported task choose none; for missing focus choose clarification or retain every perspective for open exploration.',
    }
    subsets = [list(s) for n in range(4) for s in itertools.combinations(FRAMES, n)]
    order = list(CASES)
    rng.shuffle(order)
    questions, meta = {}, {}
    for i, case in enumerate(order):
        intent_ref = 'I' + str(rng.randrange(100, 999))
        while intent_ref in state['intents']:
            intent_ref = 'I' + str(rng.randrange(100, 999))
        state['intents'][intent_ref] = case['text']
        actions = copy.deepcopy(subsets) + ['clarify']
        rng.shuffle(actions)
        criteria, mapping = {}, {}
        for label, action in zip(rng.sample(range(100, 999), 9), actions):
            option = 'K' + str(label)
            mapping[option] = sorted(action) if isinstance(action, list) else action
            criteria[option] = (
                {'action': 'Ask which relationship the user wants to explore; do not select a frame yet.'}
                if action == 'clarify' else
                {'action': 'None of the supplied perspectives addresses this request.'}
                if not action else
                {'action': 'Explore exactly this set of perspectives; no priority within this set.',
                 'perspective_refs': [aliases[k] for k in action]}
            )
        q = 'Q' + str(i + 1).zfill(3)
        questions[q] = {'type': 'choice', 'instructions': {
            'intent_ref': intent_ref,
            'question': 'Which perspective set or routing action best addresses this user intent? Use the catalog and policy; availability is not part of this decision.',
        }, 'criteria': criteria}
        meta[q] = {'case': case['id'], 'intent_ref': intent_ref, 'option_mapping': mapping,
                   'acceptable': case['acceptable'], 'annotation_reason': case['reason']}
    return {'payload': {'model': MODEL, 'state': state, 'questions': questions},
            'observer': {'frame_aliases': aliases, 'question_metadata': meta}}


def fixture():
    data = json.loads((HERE / 'fixture.json').read_text(encoding='utf-8'))
    if data != make_fixture():
        raise ValueError('frozen_fixture_mismatch')
    return data


def congruence_certificate(objects):
    sides = []
    for i in range(2):
        ring = objects['REGION_' + str(i)]['vertices']
        if len(ring) != 3:
            return {'valid': False, 'reason': 'not_two_triangles', 'tolerance': 1e-6}
        sides.append(sorted(math.dist(objects[a]['xy'], objects[ring[(j + 1) % 3]]['xy']) for j, a in enumerate(ring)))
    valid = all(abs(a - b) <= 1e-6 for a, b in zip(*sides))
    return {'valid': valid, 'reason': 'numeric_triangle_SSS' if valid else 'unequal_sorted_side_lengths',
            'sorted_side_lengths': sides, 'tolerance': 1e-6}


def dispatch(action):
    """Model decisions only select which exact code check to run, never its verdict."""
    if action == 'clarify':
        return {'action': 'clarify', 'check_work_units': 0, 'certified_bindings': [], 'unavailable_frames': []}
    if not set(action) <= set(FRAMES):
        raise ValueError('unknown_frame')
    bindings, unavailable, details = [], [], []
    for frame in action:
        found = False
        for method in geometry.METHODS:
            objects = geometry.objects_for(method, 0)
            if frame == 'congruence':
                cert = congruence_certificate(objects)
                valid = cert['valid']
            else:
                schema = geometry.GS[FRAMES[frame]['source']]
                witness = {'carrier': 'BRIDGE', 'regions': ['REGION_0', 'REGION_1'], 'host': 'HOST'}
                reasons = geometry.checker.check_witness(objects, witness, schema, 'HOST')
                cert = {'reasons': reasons, 'witness': witness}
                valid = not reasons
            details.append({'frame': frame, 'method': method, 'valid': valid, 'certificate': cert})
            if valid:
                found = True
                bindings.append({'frame': frame, 'method': method})
        if not found:
            unavailable.append(frame)
    return {'action': 'none' if not action else 'explore', 'check_work_units': len(details),
            'certified_bindings': bindings, 'unavailable_frames': unavailable, 'checks': details}


def number(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else None


def sanitize(raw, questions):
    if set(raw.get('answers', {})) != set(questions):
        raise ValueError('answer_keys')
    clean = {}
    for q, spec in questions.items():
        a = raw['answers'][q]
        if a.get('type') != 'choice' or a.get('choice') not in spec['criteria']:
            raise ValueError('typed_choice')
        probs = a.get('probabilities', {})
        if set(probs) != set(spec['criteria']):
            raise ValueError('probability_keys')
        probs = {k: number(v) for k, v in probs.items()}
        if any(v is None or not 0 <= v <= 1 for v in probs.values()) or abs(sum(probs.values()) - 1) > .02:
            raise ValueError('probabilities')
        confidence = number(a.get('confidence'))
        if confidence is not None and not 0 <= confidence <= 1:
            raise ValueError('confidence')
        if probs[a['choice']] + 1e-9 < max(probs.values()):
            raise ValueError('choice_not_argmax')
        clean[q] = {'type': 'choice', 'choice': a['choice'], 'probabilities': probs,
                    'confidence': confidence, 'reliability': number(a.get('reliability'))}
    usage = raw.get('usage', {})
    return {'answers': clean, 'usage': {k: number(usage.get(k)) for k in ('input_tokens', 'output_tokens', 'total_tokens')},
            'reliability': number(raw.get('reliability')), 'returned_model': raw.get('model') if raw.get('model') == MODEL else None}


def transport(payload):
    if os.getenv('GITHUB_ACTIONS') != 'true' or not os.getenv('TYPESAFE_API_KEY'):
        raise RuntimeError('actions_secret_required')
    import requests
    started = time.perf_counter()
    try:
        response = requests.post('https://api.typesafe.ai/v1/systemone',
                                 headers={'Authorization': 'Bearer ' + os.environ['TYPESAFE_API_KEY'],
                                          'TypeSafe-Danger-Zone-Images': 'true'}, json=payload, timeout=180)
        result = {'response': sanitize(response.json(), payload['questions'])} if response.status_code == 200 else {'failure': 'HTTP_' + str(response.status_code)}
    except Exception:
        result = {'failure': 'transport_or_choice_schema_failure'}
    result['elapsed_seconds'] = time.perf_counter() - started
    return result


def analyze(report):
    prepared = fixture()
    rows, summaries = [], {}
    answers = report.get('call', {}).get('response', {}).get('answers', {})
    for q, m in prepared['observer']['question_metadata'].items():
        text = prepared['payload']['state']['intents'][m['intent_ref']]
        actions = {'lexical': lexical(text), 'explore_all': sorted(FRAMES)}
        if q in answers:
            actions['jev'] = m['option_mapping'][answers[q]['choice']]
        for system, action in actions.items():
            execution = dispatch(action)
            acceptable = any(decision_key(action) == decision_key(a) for a in m['acceptable'])
            rows.append({'case': m['case'], 'system': system, 'selected': action,
                         'acceptable_under_author_reference': acceptable,
                         'confidence': answers[q]['confidence'] if system == 'jev' else None,
                         'execution': execution})
    for system in ('jev', 'lexical', 'explore_all'):
        rr = [r for r in rows if r['system'] == system]
        matrix = {}
        for r in rr:
            case = next(c for c in CASES if c['id'] == r['case'])
            expected = ' OR '.join(decision_key(a) for a in case['acceptable'])
            predicted = decision_key(r['selected'])
            matrix.setdefault(expected, {})[predicted] = matrix.setdefault(expected, {}).get(predicted, 0) + 1
        summaries[system] = {'cases': len(rr), 'acceptable': sum(r['acceptable_under_author_reference'] for r in rr),
                             'check_work_units': sum(r['execution']['check_work_units'] for r in rr),
                             'returned_binding_count': sum(len(r['execution']['certified_bindings']) for r in rr),
                             'unavailable_frame_selections': sum(len(r['execution']['unavailable_frames']) for r in rr),
                             'confusion_matrix_set_valued_reference': matrix}
    jev = summaries['jev']
    return {'native_choice_answers': len(answers), 'api_calls_attempted': int(bool(report.get('call'))),
            'api_failures': int('failure' in report.get('call', {})), 'systems': summaries, 'observations': rows,
            'descriptive_delta_vs_lexical': jev['acceptable'] - summaries['lexical']['acceptable'] if answers else None,
            'descriptive_work_units_avoided_vs_explore_all': summaries['explore_all']['check_work_units'] - jev['check_work_units'] if answers else None,
            'usage': report.get('call', {}).get('response', {}).get('usage', {}),
            'added_value_status': 'author_reference_pilot_only_not_established' if answers else 'not_tested'}


def viewer(out, report):
    e = html.escape
    a = report['analysis']
    body = '<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — intento e prospettive</title><style>body{font:16px system-ui;max-width:1150px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.55rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:240px;max-width:100%}details{margin:1rem 0}.note{padding:1rem;background:#edf3f7}</style><h1>Dall’intento alla prospettiva</h1>'
    body += '<p>Stato: ' + e(report['status']) + '. Una chiamata, sei Choice; tutte le combinazioni di tre prospettive, nessuna e chiarimento.</p><p class="note">JEV interpreta l’intento. Il codice controlla binding e geometria. Le immagini qui sotto servono al lettore: non vengono inviate al modello. I riferimenti semantici sono proposti dall’autore, senza validazione umana indipendente.</p>'
    body += '<table><tr><th>Sistema</th><th>Accettabili nel riferimento proposto</th><th>Controlli di codice</th><th>Binding restituiti</th></tr>'
    for system, s in a['systems'].items():
        body += '<tr><td>' + e(system) + '</td><td>' + str(s['acceptable']) + '/' + str(s['cases']) + '</td><td>' + str(s['check_work_units']) + '</td><td>' + str(s['returned_binding_count']) + '</td></tr>'
    body += '</table><p>I controlli sono unità di lavoro convenzionali (tre tagli per prospettiva), non tempi o risparmi misurati. Molti binding possono essere semanticamente non richiesti.</p>'
    for case in CASES:
        body += '<h2>' + e(case['text']) + '</h2><p>Azioni accettabili proposte: ' + e(' oppure '.join(decision_key(v) for v in case['acceptable'])) + '.</p><table><tr><th>Sistema</th><th>Selezione</th><th>Coerente</th><th>Prospettive senza binding</th></tr>'
        for row in [r for r in a['observations'] if r['case'] == case['id']]:
            body += '<tr><td>' + e(row['system']) + '</td><td>' + e(decision_key(row['selected'])) + '</td><td>' + ('sì' if row['acceptable_under_author_reference'] else 'no') + '</td><td>' + e(', '.join(row['execution']['unavailable_frames']) or '—') + '</td></tr>'
        body += '</table>'
    body += '<h2>Workspace e tre costruzioni controllate dal codice</h2>'
    for method in geometry.METHODS:
        body += '<figure style="display:inline-block"><img src="images/' + method + '.png" alt="Taglio del workspace verificato dal codice"><figcaption>' + method + '</figcaption></figure>'
    for title, value in [('Catalogo e provenienza', report['catalog_provenance']), ('Input esatto e annotazioni esterne', report['prepared']), ('Risposta nativa sanificata', report.get('call')), ('Analisi completa', a), ('Limiti', LIMITS)]:
        body += '<details><summary>' + title + '</summary><pre>' + e(json.dumps(value, ensure_ascii=False, indent=2)) + '</pre></details>'
    body += '<p><a href="PROTOCOL.md">Protocollo</a> · <a href="VERIFIED_RESULTS.md">Risultati verificati</a> · <a href="results.json">Dati</a></p></html>'
    (out / 'viewer.html').write_text(body, encoding='utf-8')


def save(out, report):
    report['analysis'] = analyze(report)
    temp = out / 'results.tmp'
    temp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(out / 'results.json')
    viewer(out, report)


def main(out, live=False):
    if live and (os.getenv('GITHUB_ACTIONS') != 'true' or not os.getenv('TYPESAFE_API_KEY')):
        raise SystemExit('Actions and repository secret required')
    out.mkdir(parents=True, exist_ok=True)
    # Reader-only illustrations are never part of make_fixture()/the API input.
    for method in geometry.METHODS:
        geometry.render(geometry.objects_for(method, 0), {k: k for k in 'ABCDEF'}, out / 'images' / (method + '.png'))
    for name in ('PROTOCOL.md', 'VERIFIED_RESULTS.md'):
        if (HERE / name).exists():
            (out / name).write_text((HERE / name).read_text(encoding='utf-8'), encoding='utf-8')
    prepared = fixture()
    report = {'experiment': 'Semantic perspective routing v1', 'model': MODEL,
              'status': 'running' if live else 'offline_only', 'run_id': os.getenv('GITHUB_RUN_ID'),
              'source_commit': os.getenv('GITHUB_SHA'), 'parent_commit': PARENT, 'limits': LIMITS,
              'prepared': prepared, 'request_sha256': digest(prepared['payload']),
              'fixture_sha256': digest(prepared),
              'catalog_provenance': {'historical_memory_sha256': hashlib.sha256(geometry.native.MEMORY_PATH.read_bytes()).hexdigest(),
                                     'frames': FRAMES, 'historical_entries': [geometry.native.ENTRIES[FRAMES[k]['source']] for k in ('triangles', 'polyrole')],
                                     'grammar_source': 'experiments/native_score_fanout/benchmark_scores.py::schemas'},
              'workspace_inventory_observer_only': dispatch(sorted(FRAMES))}
    save(out, report)
    if live:
        report['call'] = transport(prepared['payload'])
        report['status'] = 'completed' if 'response' in report['call'] else 'failed'
        save(out, report)
        if report['status'] != 'completed':
            raise SystemExit('Single call failed; sanitized failure saved; no retry')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path('output_semantic_perspective_routing'))
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--freeze', action='store_true')
    args = ap.parse_args()
    if args.freeze:
        if args.live:
            raise SystemExit('Freeze offline before live')
        (HERE / 'fixture.json').write_text(json.dumps(make_fixture(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        main(args.out, args.live)
