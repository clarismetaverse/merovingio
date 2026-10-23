# Merovingio v6 — Productivity-Driven Opposition REBASE

## Ipotesi

La v5 seleziona opposizioni angolo-lato in base alla vicinanza topologica. La v6 introduce una seconda pressione: la capacità di un nuovo binding di istanziare o completare un **Generic Space parziale**, generato dalla costruzione mediale CD.

Si rimane esclusivamente sulle opposizioni ANGLES ↔ SIDES; non c'è rebase di triangoli o criterio LAL.

## Funzionamento

1. Il grafo geometrico v2 ricava tutte le opposizioni reali angolo-lato.
2. La v3 ricava le partizioni angolari e segmentali con la stessa origine costruttiva, generando gli slot astratti dei Generic Spaces.
3. Il primo binding può creare un Generic Space INCOMPLETE con un'opposizione ancora da cercare.
4. Ogni prossimo REBASE viene valutato per la novità delle relazioni che può completare, senza fornire come etichetta la risposta finale.
5. Il punteggio PROSPECTIVE è precedente alla selezione; il feedback PRODUCTIVITY viene invece emesso dopo un GS effettivamente formato. Il feedback può aumentare la salienza della seconda opposizione, non dichiararne vera la relazione metrica.
6. Un GS che allinea opposizioni di provenienze differenti può essere registrato, ma non viene ricompensato come co-generato dalla stessa costruzione.

La domanda dall'uguaglianza angolare verso AD = DB? rimane una ipotesi, non una prova. Nel controllo scaleno la divisione angolare non rende uguali le porzioni della base. Una trasversale che non è bisettrice produce partizioni ma non fornisce la relazione angolare sorgente.

## Ablazioni

- fixed_initial: baseline statica forte.
- topology_only: ranking dinamico e propagazione v5.
- predictive_only: score prospettico del completamento, senza feedback effettivo.
- productivity_feedback: score prospettico più feedback dai GS che emergono.
- feedback_genealogy_blind: stessa struttura con genealogia nascosta nel ranking e feedback attenuato.

## Due condizioni iniziali, identica geometria

- clean: salienza all'angolo costruito.
- competing_oppositions: si attivano altre due opposizioni reali e non co-generate dalla costruzione CD, senza alterare la figura o le condizioni matematiche.

Test con 4 REBASE per 32 seed, 5 strategie, 3 geometrie e 2 condizioni di attenzione.

## Misure

Completamento del Generic Space, step della prima chiusura, generazione della domanda lecita, feedback causalmente prodotto da nuove Gestalten, ranking ricalcolato, false asserzioni metriche (devono rimanere zero).

Il modello è costruito manualmente. Non costituisce una prova che Euclide o i soggetti umani ragionassero così. Un vantaggio del ranking statico deve essere riportato, non nascosto.

## Riprodurre da root repo

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v6 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v6/productive.py --seeds 32 --budget 4
    python NMerovingio/experiments/gestalt_heat_v6/viewer.py

Output: results/traces.json, results/aggregates.json, results/REPORT.md, results/viewer.html.
