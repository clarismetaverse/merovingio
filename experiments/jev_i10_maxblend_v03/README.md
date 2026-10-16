# Merovingio v0.3 — I.10, ricerca costruttiva **senza dimostrazione**

**Stato:** prototipo locale funzionante + adapter Jev Vision non ancora eseguito su API live.

## La domanda sperimentale

> Conosciamo tre Mental Spaces: segmento AB, angolo al vertice C, triangolo equilatero ABC. Senza mostrare la prova o la conclusione di I.10, quale costruzione realizza la maggiore *coerenza strutturale dei raggruppamenti misti lati–angoli*?

Questo **non** è un dimostratore della proposizione I.10. In particolare non tenta di derivare `AD = DB`, non invoca LAL, non seleziona I.4 e non etichetta nel prompt Jev il criterio/la costruzione vincente. Il sistema confronta **conseguenze strutturali candidate** di costruzioni geometricamente ammissibili.

## Contenuto

- `src/prototype.py`: costruzioni candidate, deduplicazione geometrica, Mental Spaces/Generic Spaces con provenance, baseline esplicita, PNG, adapter Jev.
- `src/make_viewer.py`: visualizzatore offline.
- `tests/test_experiment.py`: sei test automatici inclusi controllo di leakage.
- `output/index.html`: viewer pronto; aprirlo con browser (oppure via un server HTTP statico).
- `output/images/*.png`: figura iniziale e trasformazioni (con e senza raggruppamenti colorati).
- `output/results.json`: strutture cognitive candidate e punteggi **euristici**, non risultati Jev.

## Esecuzione locale

```bash
python -m pip install -r requirements.txt
python src/prototype.py --out output
python src/make_viewer.py output
python -m unittest discover -s tests -v
```

Apri `output/index.html` e scegli i candidati C01...C05 e i tre livelli **figura iniziale / costruzione / regrouping**.

## Jev Vision, opzionale

La connessione live non viene eseguita automaticamente. Richiede una chiave personale:

```bash
export TYPESAFE_API_KEY='...'
python src/prototype.py --out output --jev
```

Il client usa `POST https://api.typesafe.ai/v1/systemone`, `model=jev-1.14.0`, `Authorization: Bearer ...`, `TypeSafe-Danger-Zone-Images: true` e `assets` PNG base64 come descritti nella [documentazione ufficiale](https://docs.typesafe.ai/images) e nelle [choice questions](https://docs.typesafe.ai/primitives/choice).

Ogni candidata è inviata come immagine nello `state` con **ID anonimizzato**, senza operation label. Jev seleziona una configurazione con `choice` e assegna uno `score` di compatibilità a ciascuna. *Le domande nello stesso batch non rappresentano un ragionamento sequenziale.*

Il report live finisce in `output/jev_live_response.json`. Se la chiave è assente, il programma fallisce esplicitamente e non finge risultati del modello. **Non salvare chiavi API nel repository.**

## Esperimento attuale

Il construction engine genera sette operazioni, che diventano cinque configurazioni geometricamente distinte: nel triangolo equilatero le costruzioni di bisettrice, mediana e altezza dal vertice C coincidono e quindi sono **deduplicate**.

L'euristica locale registra un allineamento di ruoli fra i gruppi ai due lati della nuova connessione (outer side, shared carrier, included wedge) senza invocare alcun criterio di congruenza. Un mismatch angolare è calcolato numericamente da coordinate generate; questo rappresenta un segnale **simulato**, non una proprietà già dimostrata formalmente.

Lo score misura solo un possibile *proxy* del valore del blending; usa coefficienti arbitrari, non un apprendimento. Il fatto che in questo singolo caso valorizzi l'asse centrale **non dimostra** che l'ipotesi cognitiva generalizzi. La simmetria visiva costituisce un serio fattore confondente.

## Grounding / status epistemico

- `given`: segmento AB e triangolo equilatero ABC (vincolo iniziale);
- `construction_identity`: oggetti condivisi / incidenze prodotte;
- `measured_visual_candidate`: allineamenti stimati numericamente/visivamente;
- `candidate`: Generic Spaces plausibili;
- **nessun** `theorem_proven` o `goal_reached`.

Provenance e ordine: AB → equilatero ABC → costruzione candidata → raggruppamenti nuovi → Generic Space candidato.

## Limiti e prossimi test

1. Eseguire Jev Vision con chiave effettiva e registrare `answers`, probabilità e latenza.
2. Mescolare l'ordine e i codici delle candidate fra prove per impedire `position bias`.
3. Variare nomi dei vertici, rotazioni, scale e forme triangolari, anche non simmetriche.
4. Confrontare immagini sole, rappresentazione simbolica sola e combinazione.
5. Valutare **nuove connessioni verificate** contro una baseline che favorisce solo la simmetria visiva.
6. Solo più avanti integrare frame selection, role binding e dimostrazione.

## Fonti API

- https://docs.typesafe.ai/images
- https://docs.typesafe.ai/primitives/choice
- https://docs.typesafe.ai/api
- https://typesafe.ai/blog/jev-1-14

## GitHub Actions — first live Jev Vision trial

The repository workflow `.github/workflows/jev-i10-maxblend.yml` runs on
push to the dedicated experiment branch. It reads the repository secret
`TYPESAFE_API_KEY` only in the live API step, and uploads a **sanitized**
`output/jev_summary.json` as an Actions artifact. Do not put secrets in
source code, `workflow_dispatch` inputs, logs or git history.

The live runner `src/run_jev_ci.py` sends the **unannotated** candidate diagrams
(the `_raw.png` assets). It asks Jev 1.14 to rank mixed side-angle regroupings
without the proposition's goal or answer. This experiment does not prove I.10.
The summary includes choice probabilities, scores, model version, usage and
baseline comparison. A completed workflow is required before claiming Jev results.