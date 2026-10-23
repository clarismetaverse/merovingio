"""Eight visual next-step choices: same final segment, different moving endpoints."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import html
import json
import math
import os
from pathlib import Path
import random
import sys
import uuid

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'experiments/semantic_perspective_routing'))
import benchmark_routing as native

MODEL = 'jev-1.14.0'
SEED = 2026102309
PARENT = '90083c9c27e8ecd48bd81668c46b25bb38ba46fb'
CONDITIONS = ('final_only', 'images', 'text_history', 'combined')
HISTORIES = ('move_A', 'move_B')
COLORS = {'A': (0, 114, 178), 'B': (230, 159, 0)}
TITLE = {'final_only': 'Solo stato finale', 'images': 'Cronologia visiva',
         'text_history': 'Cronologia testuale, opzioni visive', 'combined': 'Cronologia visiva + testuale'}
INSTRUCTIONS = ('Choose the next picture that continues the observed change by ONE EQUAL STEP: '
                'keep the previously stationary endpoint fixed and move the changing endpoint by its previous per-step displacement. '
                'The observations are earliest to latest. This is continuation of a demonstrated edit, not a theorem. '
                'If the observations do not determine which endpoint was changing, choose insufficient evidence. '
                'An unchanged segment is an actual proposed edit, distinct from insufficient evidence.')
LIMITS = [
    'Eight independent requests, one native Choice each: two histories x four evidence conditions. No extra questions, retries, composites, confidence thresholds or repair calls.',
    'Both histories have exactly the same final PNG and candidate images. In one only A moves outwards, in the other only B. Full evidence plus an explicit equal-step continuation rule determines a unique next edit.',
    'Final-only is non-identifiable. Next-step accuracy is null there; report unsupported proposals and insufficient-evidence behavior separately. The two preplanned final-only requests are byte-identical and are not retries.',
    'Text-history has no past-frame image observations but retains visual candidate criteria. It tests textual history PLUS visual option matching, not an entirely text-only model input.',
    'All histories use the same rotated/reflected coordinates, endpoint identities, palette, option order and codes. Blue/amber identify A/B, not correctness. One transform, one scale, two templates: no generalization estimate.',
    'The raster tracker reads colored endpoint centers from the actual PNGs and matches predicted coordinates to the candidate PNGs. It receives no history name, gold, scene coordinates or renderer metadata. It assumes this clean palette and separable endpoint markers; no general vision system is claimed.',
    'The text tracker computes endpoint displacements from supplied coordinates and matches candidate PNG endpoint centers. Combined reports both trackers. Their checks do not establish autonomous extraction of workspace topology.',
    'Code checks collinearity, unchanged endpoint, segment length and equal-step extrapolation independently of Jev. Choosing a supplied next-view is not free-form construction generation or exact coordinate generation by the model.',
    'The explicit constant-displacement rule supplies the extrapolation policy. Sequences alone cannot establish unique human intention. Accuracy measures this bounded imitation task, not geometric proof or internal sequential reasoning.',
    'A sequence advantage over final-only would show use of additional observations, not a necessity of three frames: two distinct endpoint observations suffice under the supplied rule. No middle-only, shuffled-order or reverse-order live ablation is included in the eight-question budget.',
    'Image options include inward edits, outward edits at either endpoint, and no change; all are valid nondegenerate collinear segments, but not all are prolongations. Insufficient evidence is a separate text option.',
    'Native probabilities, confidence, usage and numeric reliability if supplied are preserved. Missing values remain null. Latency is descriptive and no speed or cost advantage over tracking is assumed.',
]


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()


def point(x, y=0, reflected=True):
    # Exact 3-4-5 rotation and one reflection, avoiding subpixel baseline ambiguity.
    u = -x if reflected else x
    return [round(192 + .8 * u - .6 * y, 8), round(192 + .6 * u + .8 * y, 8)]


def observations(history):
    if history not in HISTORIES:
        raise ValueError('history')
    return [{'A': point(-25 - 25 * i), 'B': point(75)} if history == 'move_A'
            else {'A': point(-75), 'B': point(25 + 25 * i)} for i in range(3)]


def candidates():
    return {'extend_A': {'A': point(-100), 'B': point(75)},
            'extend_B': {'A': point(-75), 'B': point(100)},
            'shorten_A': {'A': point(-50), 'B': point(75)},
            'shorten_B': {'A': point(-75), 'B': point(50)},
            'hold': {'A': point(-75), 'B': point(75)}}


def render(scene):
    im = Image.new('RGB', (384, 384), 'white')
    draw = ImageDraw.Draw(im)
    draw.line([tuple(scene[k]) for k in ('A', 'B')], fill='#26313d', width=4)
    font = ImageFont.load_default(size=18)
    for k in ('A', 'B'):
        x, y = map(round, scene[k])
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=COLORS[k])
        draw.text((x + 9, y + 6), k, fill='#26313d', font=font)
    return im


def freeze():
    rng = random.Random(SEED)
    scenes = {'current': observations('move_A')[-1]}
    for h in HISTORIES:
        for i, scene in enumerate(observations(h)):
            scenes[h + '_' + str(i)] = scene
    scenes.update(candidates())
    by_scene, assets, refs = {}, [], {}
    for name, scene in scenes.items():
        key = digest(scene)
        if key not in by_scene:
            asset = str(uuid.UUID(int=rng.getrandbits(128)))
            path = Path('images') / (asset + '.png')
            target = HERE / 'fixtures' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            render(scene).save(target)
            by_scene[key] = asset
            assets.append({'asset': asset, 'file': path.as_posix(), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        refs[name] = by_scene[key]
    actions = list(candidates()) + ['insufficient']
    rng.shuffle(actions)
    mapping = dict(zip(['K' + str(n) for n in rng.sample(range(100, 999), 6)], actions))
    events = [(h, c) for h in HISTORIES for c in CONDITIONS]
    rng.shuffle(events)
    manifest = {'seed': SEED, 'assets': assets, 'scene_asset_refs': refs,
                'option_mapping': mapping, 'event_order': events,
                'renderer': {'canvas': [384, 384], 'rotation_cos_sin': [.8, .6], 'reflection': -1,
                             'line_width': 4, 'endpoint_radius': 6, 'point_colors': COLORS}}
    (HERE / 'fixtures/manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


def manifest():
    return json.loads((HERE / 'fixtures/manifest.json').read_text(encoding='utf-8'))


def next_prediction(snapshots, tolerance=1.):
    if len(snapshots) < 2:
        return None
    diffs = {k: [[snapshots[i][k][j] - snapshots[i - 1][k][j] for j in (0, 1)]
                 for i in range(1, len(snapshots))] for k in ('A', 'B')}
    moving = [k for k in diffs if any(math.hypot(*d) > tolerance for d in diffs[k])]
    if len(moving) != 1:
        return None
    k = moving[0]
    if any(math.dist(d, diffs[k][0]) > tolerance for d in diffs[k]):
        return None
    result = copy.deepcopy(snapshots[-1])
    result[k] = [result[k][j] + sum(d[j] for d in diffs[k]) / len(diffs[k]) for j in (0, 1)]
    return result


def geometry_certificate(scene):
    current = observations('move_A')[-1]
    a, b = current['A'], current['B']
    dx, dy = b[0] - a[0], b[1] - a[1]
    cross = [dx * (p[1] - a[1]) - dy * (p[0] - a[0]) for p in scene.values()]
    length = math.dist(scene['A'], scene['B'])
    changed = [k for k in ('A', 'B') if math.dist(scene[k], current[k]) > 1e-8]
    u = [scene['B'][j] - scene['A'][j] for j in (0, 1)]
    projections = [sum((p[j] - scene['A'][j]) * u[j] for j in (0, 1)) / length**2 for p in (a, b)] if length > 1e-8 else []
    contains = bool(projections) and all(-1e-8 <= t <= 1 + 1e-8 for t in projections) and all(abs(v) < 1e-8 for v in cross)
    return {'nondegenerate': length > 1e-8, 'collinear_with_current': all(abs(v) < 1e-8 for v in cross),
            'length': length, 'changed_endpoints': changed,
            'contains_current_segment': contains,
            'strict_extension': contains and length > math.dist(a, b) + 1e-8 and len(changed) == 1,
            'equal_step_size_if_changed': all(abs(math.dist(scene[k], current[k]) - 25) < 1e-8 for k in changed)}


def build_payload(out, history, condition):
    if history not in HISTORIES or condition not in CONDITIONS:
        raise ValueError('unknown_cell')
    m = manifest()
    refs = m['scene_asset_refs']
    criteria = {}
    for option, action in m['option_mapping'].items():
        criteria[option] = {'description': 'The observations do not determine a unique next edit.'} if action == 'insufficient' else {'next_view': refs[action]}
    frames = []
    for i in ([2] if condition == 'final_only' else range(3)):
        frame = {'step': i}
        if condition != 'text_history':
            frame['image'] = refs[history + '_' + str(i)]
        if condition in ('text_history', 'combined'):
            frame['endpoint_coordinates'] = observations(history)[i]
        frames.append(frame)
    state = {'workspace': 'One segment with stable endpoint identities across observations and candidate images.',
             'point_identity': {'A': 'blue marker', 'B': 'amber marker'},
             'coordinate_convention': 'Image pixels: origin top left, x increases rightward and y downward.',
             'observation_order': 'earliest to latest', 'observations': frames}
    p = {'model': MODEL, 'state': state, 'questions': {'next': {'type': 'choice', 'instructions': INSTRUCTIONS, 'criteria': criteria}}}
    used = set()
    def collect(v):
        if isinstance(v, str) and v in {a['asset'] for a in m['assets']}:
            used.add(v)
        elif isinstance(v, dict):
            for x in v.values():
                collect(x)
        elif isinstance(v, list):
            for x in v:
                collect(x)
    collect(p)
    p['assets'], audit = {}, []
    for asset in m['assets']:
        if asset['asset'] not in used:
            continue
        data = (HERE / 'fixtures' / asset['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != asset['sha256']:
            raise ValueError('frozen_image_mismatch')
        target = out / asset['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        p['assets'][asset['asset']] = {'type': 'image', 'format': 'png', 'data_base64': base64.b64encode(data).decode('ascii')}
        audit.append(asset)
    predicted = next_prediction(observations(history))
    reference = next(k for k, scene in candidates().items() if scene == predicted) if condition != 'final_only' else None
    observer = {'history': history, 'condition': condition, 'option_mapping': m['option_mapping'],
                'reference_next_action': reference, 'reference_response': reference or 'insufficient',
                'identifiable': condition != 'final_only', 'numeric_history_observer_only': observations(history),
                'candidate_certificates_observer_only': {k: geometry_certificate(v) for k, v in candidates().items()}}
    return p, observer, audit


def raster_endpoints(path):
    """Only inspect image pixels; no scene, source history or model verdict is used."""
    with Image.open(path) as image:
        pixels = list(image.convert('RGB').getdata())
        width = image.width
    result = {}
    for name, color in COLORS.items():
        hits = [(i % width, i // width) for i, p in enumerate(pixels) if p == color]
        if not hits:
            raise ValueError('endpoint_marker_not_found')
        result[name] = [sum(p[j] for p in hits) / len(hits) for j in (0, 1)]
    return result


def tracker(payload, out, evidence):
    paths = {a['asset']: out / a['file'] for a in manifest()['assets']}
    frames = payload['state']['observations']
    if evidence == 'raster':
        if any('image' not in frame for frame in frames):
            return None
        snapshots = [raster_endpoints(paths[frame['image']]) for frame in frames]
    elif evidence == 'coordinates':
        if any('endpoint_coordinates' not in frame for frame in frames):
            return None
        snapshots = [frame['endpoint_coordinates'] for frame in frames]
    else:
        raise ValueError('tracker_evidence')
    prediction = next_prediction(snapshots)
    if prediction is None:
        return 'insufficient'
    matches = []
    for option, value in payload['questions']['next']['criteria'].items():
        if 'next_view' not in value:
            continue
        actual = raster_endpoints(paths[value['next_view']])
        if all(math.dist(actual[k], prediction[k]) <= 1. for k in ('A', 'B')):
            matches.append(option)
    if len(matches) != 1:
        return 'insufficient'
    return manifest()['option_mapping'][matches[0]]


def analyze(calls):
    rows = []
    for c in calls:
        answer = c.get('response', {}).get('answers', {}).get('next')
        selected = c['option_mapping'][answer['choice']] if answer else None
        r = {'condition': c['condition'], 'history': c['history'], 'identifiable': c['identifiable'],
             'reference_next_action': c['reference_next_action'], 'reference_response': c['reference_response'],
             'selected': selected, 'next_step_correct': selected == c['reference_next_action'] if c['identifiable'] and selected is not None else None,
             'evidence_policy_correct': selected == c['reference_response'] if selected is not None else None,
             'confidence': answer['confidence'] if answer else None, 'failure': c.get('failure'),
             'trackers': c['baseline_predictions'],
             'selected_geometry': c['candidate_certificates_observer_only'].get(selected),
             'probabilities_by_action': {c['option_mapping'][k]: v for k, v in answer['probabilities'].items()} if answer else None}
        rows.append(r)
    groups = {}
    for condition in CONDITIONS:
        rr = [r for r in rows if r['condition'] == condition]
        answered = [r for r in rr if r['selected'] is not None]
        matrix = {}
        for r in answered:
            reference = r['reference_next_action'] or 'non_identifiable'
            matrix.setdefault(reference, {})[r['selected']] = matrix.setdefault(reference, {}).get(r['selected'], 0) + 1
        groups[condition] = {'prepared': len(rr), 'answered': len(answered),
                             'next_step_correct': sum(r['next_step_correct'] is True for r in answered) if condition != 'final_only' else None,
                             'next_step_accuracy': sum(r['next_step_correct'] is True for r in answered) / len(rr) if condition != 'final_only' and answered else None,
                             'insufficient_evidence': sum(r['selected'] == 'insufficient' for r in answered),
                             'unsupported_next_step_proposals': sum(r['selected'] != 'insufficient' for r in answered) if condition == 'final_only' else None,
                             'control_policy_correct': sum(r['evidence_policy_correct'] is True for r in answered) if condition == 'final_only' else None,
                             'confusion_matrix': matrix,
                             'matched_tracker_next_step_correct': sum(r['trackers']['matched'] == r['reference_next_action'] for r in rr) if condition != 'final_only' else None,
                             'matched_tracker_control_abstentions': sum(r['trackers']['matched'] == 'insufficient' for r in rr) if condition == 'final_only' else None}
    paired = {}
    for first, second in (('images', 'text_history'), ('images', 'combined'), ('text_history', 'combined')):
        aa = {r['history']: r for r in rows if r['condition'] == first and r['selected'] is not None}
        bb = {r['history']: r for r in rows if r['condition'] == second and r['selected'] is not None}
        keys = aa.keys() & bb.keys()
        paired[first + '_to_' + second] = {'pairs': len(keys), 'improved': sum(not aa[k]['next_step_correct'] and bb[k]['next_step_correct'] for k in keys),
                                          'worsened': sum(aa[k]['next_step_correct'] and not bb[k]['next_step_correct'] for k in keys)}
    usage = {k: sum(c['response']['usage'][k] for c in calls if c.get('response', {}).get('usage', {}).get(k) is not None)
             if any(c.get('response', {}).get('usage', {}).get(k) is not None for c in calls) else None for k in ('input_tokens', 'output_tokens', 'total_tokens')}
    return {'native_choice_answers': sum('response' in c for c in calls), 'api_calls_attempted': sum('response' in c or 'failure' in c for c in calls),
            'api_failures': sum('failure' in c for c in calls), 'by_condition': groups, 'observations': rows,
            'paired_descriptive_changes': paired, 'usage_totals': usage}


def viewer(out, r):
    e = html.escape
    m = manifest()
    files = {a['asset']: a['file'] for a in m['assets']}
    def picture(ref, caption):
        return '<figure><img src="' + files[ref] + '" alt="Segmento con identità dei punti stabili"><figcaption>' + e(caption) + '</figcaption></figure>'
    body = '<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — continuazione del segmento</title><style>body{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:205px;max-width:100%}figure{display:inline-block;margin:.4rem}details{margin:1rem 0}.note{padding:1rem;background:#edf3f7}</style><h1>Stesso segmento finale, due continuazioni</h1><p>Stato: ' + e(r['status']) + '. Otto domande, una per contesto indipendente.</p><p class="note">A blu e B ambra indicano identità, non risposte. Entrambe le storie terminano nello stesso PNG. Il controllo finale non ha una continuazione unica: la sua accuratezza geometrica resta indefinita. La regola di continuazione a passo costante è fornita.</p>'
    for history in HISTORIES:
        body += '<h2>' + ('Cresce da A' if history == 'move_A' else 'Cresce da B') + '</h2>'
        for i in range(3):
            body += picture(m['scene_asset_refs'][history + '_' + str(i)], 'Osservazione ' + str(i))
    body += '<h2>Alternative visive comuni</h2>'
    for action in candidates():
        body += picture(m['scene_asset_refs'][action], action + ' — descrizione solo per il lettore')
    body += '<table><tr><th>Evidenza</th><th>JEV: passo corretto</th><th>Astensioni</th><th>Proposte non supportate nel controllo</th><th>Tracker: passo corretto</th></tr>'
    for c, s in r['analysis']['by_condition'].items():
        score = str(s['next_step_correct']) + '/2' if s['next_step_correct'] is not None else 'non identificabile'
        if not s['answered']:
            score = 'non eseguito'
        body += '<tr><td>' + TITLE[c] + '</td><td>' + score + '</td><td>' + str(s['insufficient_evidence']) + '</td><td>' + str(s['unsupported_next_step_proposals']) + '</td><td>' + (str(s['matched_tracker_next_step_correct']) + '/2' if c != 'final_only' else 'astensione: ' + str(s['matched_tracker_control_abstentions']) + '/2') + '</td></tr>'
    body += '</table><p>“Cronologia testuale” conserva opzioni visive: non è una condizione senza immagini. I due controlli finali sono richieste identiche pianificate prima del live. Una sola trasformazione controllata, nessuna stima di generalizzazione.</p>'
    for row in r['analysis']['observations']:
        body += '<p><strong>' + e(row['history'] + ' / ' + row['condition']) + '</strong>: ' + e(str(row['selected'])) + '; confidenza ' + e(str(row['confidence'])) + '; baseline ' + e(str(row['trackers']['matched'])) + '.</p>'
    for title, value in [('Probabilità, matrici e confronti', r['analysis']), ('Input e risposte native sanificate', r['calls']), ('Regola e limiti', LIMITS)]:
        body += '<details><summary>' + title + '</summary><pre>' + e(json.dumps(value, indent=2, ensure_ascii=False)) + '</pre></details>'
    body += '<p><a href="PROTOCOL.md">Protocollo</a> · <a href="VERIFIED_RESULTS.md">Risultati verificati</a> · <a href="results.json">Dati</a></p></html>'
    (out / 'viewer.html').write_text(body, encoding='utf-8')


def save(out, r):
    r['analysis'] = analyze(r['calls'])
    temp = out / 'results.tmp'
    temp.write_text(json.dumps(r, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(out / 'results.json')
    viewer(out, r)


def main(out, live=False):
    if live and (os.getenv('GITHUB_ACTIONS') != 'true' or not os.getenv('TYPESAFE_API_KEY')):
        raise SystemExit('Actions and repository secret required')
    out.mkdir(parents=True, exist_ok=True)
    for a in manifest()['assets']:
        target = out / a['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        data = (HERE / 'fixtures' / a['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != a['sha256']:
            raise ValueError('frozen_image_mismatch')
        target.write_bytes(data)
    for name in ('PROTOCOL.md', 'VERIFIED_RESULTS.md'):
        if (HERE / name).exists():
            (out / name).write_text((HERE / name).read_text(encoding='utf-8'), encoding='utf-8')
    r = {'experiment': 'Segment continuation v1', 'status': 'running' if live else 'offline_only',
         'model': MODEL, 'run_id': os.getenv('GITHUB_RUN_ID'), 'source_commit': os.getenv('GITHUB_SHA'),
         'parent_commit': PARENT, 'fixture_manifest_sha256': digest(manifest()), 'limits': LIMITS, 'calls': []}
    save(out, r)
    for history, condition in manifest()['event_order']:
        p, observer, audit = build_payload(out, history, condition)
        pixel = tracker(p, out, 'raster')
        text = tracker(p, out, 'coordinates')
        record = {**observer, 'model_input': {k: v for k, v in p.items() if k != 'assets'},
                  'asset_audit': audit, 'request_sha256': digest(p),
                  'baseline_predictions': {'raster': pixel, 'coordinates': text, 'matched': text if condition == 'text_history' else pixel}}
        if live:
            record.update(native.transport(p))
        r['calls'].append(record)
        save(out, r)
        print('Recorded', len(r['calls']), '/8', flush=True)
        if record.get('failure') in ('HTTP_400', 'HTTP_401', 'HTTP_403'):
            r['status'] = 'request_rejected'
            save(out, r)
            raise SystemExit('Rejected; sanitized artifact saved, no retries')
    r['status'] = 'completed_with_failures' if any('failure' in c for c in r['calls']) else 'completed' if live else 'offline_only'
    save(out, r)
    if r['status'] == 'completed_with_failures':
        raise SystemExit('Sanitized failures saved')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path('output_segment_continuation'))
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--freeze', action='store_true')
    args = ap.parse_args()
    if args.freeze:
        if args.live:
            raise SystemExit('Freeze offline before live')
        freeze()
    else:
        main(args.out, args.live)
