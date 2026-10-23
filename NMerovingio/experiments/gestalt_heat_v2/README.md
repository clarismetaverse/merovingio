# Merovingio · Gestalt Propagation v2: raggruppamenti generati, non enumerati

## Domanda cognitiva
Una pressione analogica già attiva fra i macrogruppi ANGLES e SIDES può orientare **la formazione stessa** dei sottogruppi visivi, prima che esistano tutti i Mental Spaces? E le analogie rese disponibili dai sottogruppi possono modificare la pressione iniziale?

Il caso di studio è la bisettrice CD in Euclide I.10. Il ragionamento cercato parte dalla partizione angolare e dall'opposizione visiva angolo ↔ lato nelle nuove sottofigure. La tensione orientata parte da ∠ACD = ∠DCB (costruito) e cerca se la relazione possa essere analogicamente proiettata su AD, DB (HYPOTHESIS_ONLY). CD incide su AB creando nuove estremità, segmenti e triangoli. L'uguaglianza dei segmenti non viene mai inferita direttamente dagli angoli.

## Differenza decisiva rispetto alla v1
La v1 aveva un elenco esplicito di gruppi da selezionare (ANGLE_PAIR, BASE_PAIR, OPPOSITION_PAIR, SAS_TRIPLETS). La v2 **non enumera questi gruppi**.

1. Ricostruisce un grafo dopo la costruzione a partire da vertici, segmenti, cicli triangolari geometricamente non degeneri e relazioni: endpoint, boundary, angle_in_region, bounds_angle, opposite, part_of, equal_given, share_material_side.
2. La grammatica genera in tempo di ricerca codelets SEED (per qualunque relazione osservata), EXTEND (una nuova relazione incidente a un gruppo già formato), ALIGN (due istanze distinte della medesima struttura relazionale).
3. Un eventuale Generic Space viene indotto dall'allineamento di due istanze della stessa signature di ruolo, preservandone la genealogia.
4. La macro-tensione ANGLES↔SIDES aumenta le probabilità di esplorare relazioni angolo-lato e opposizioni, non gruppi etichettati con la risposta attesa.
5. Nella condizione reciproca ciascun gruppo selezionato riattiva i macroconcetti che mobilita. Nel controllo reciprocal_without_opposition viene ablata la sola pressione dell'opposizione, mantenendo attivi altri macrodomini e feedback.
6. Un allineamento di due coppie ANGLE–opposite–SIDE con gli angoli noti uguali può produrre un candidato di slippage ANGLE equality→SIDE equality, marcato HYPOTHESIS_ONLY. Nessuna licenza dimostrativa viene emessa.

Gli operatori relazionali sono tuttora definiti manualmente. Quindi si tratta di generazione combinatoria endogena di gruppi, non di invenzione neurale del vocabolario dei concetti.

## Quattro condizioni
- bottom_up: attivazione macro zero, solo affordance del grafo.
- feedforward: macro-attivazione lato/angolo/opposizione, nessun feedback.
- reciprocal: macro-attivazione iniziale più feedback micro→macro.
- reciprocal_without_opposition: stessa architettura reciproca ma macro-opposizione disattivata forzatamente.

Geometria, budget, operatori e seed comparabili per tutte le condizioni. Due triangoli: isoscele e scaleno. Lo scaleno non è un esempio di bisettrice-mediana: D è costruito secondo il rapporto AC:BC. Le distanze osservate non sono usate per certificare il target.

## Epistemologia
- Incidenza, cicli triangolari e opposizione sono relazioni geometriche strutturali.
- La congruenza dei due settori angolari è garantita dalla bisettrice costruita.
- L'ipotizzata congruenza AD = DB **non è** misura verificata né dimostrazione.
- L'analogia non modifica il grafo materiale: modifica le priorità dei codelets.
- L'esperimento misura una simulazione progettata: non dimostra un processo storico di Euclide né una legge psicologica.

## Fonti nel repository
- NMerovingio/graph/examples/generic_spaces_v0_8.json
- NMerovingio/graph/generic_space_memory_v0_9.json
- NMerovingio/experiments/gestalt_heat_v1/engine.py

## Eseguire dalla root del repo

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v2 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v2/endogenous.py --seeds 32 --budget 16
    python NMerovingio/experiments/gestalt_heat_v2/viewer.py

Output: results/traces.json, results/aggregate.json, results/REPORT.md, results/viewer.html. Il viewer mostra ogni passaggio e le attivazioni del sistema.
