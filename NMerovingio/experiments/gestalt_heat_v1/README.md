# Gestalt Heat v1 — Propagazione macro↔micro delle opposizioni lato–angolo

**Stato:** simulazione cognitiva con codelets seedati, non test umano, non Copycat originale, senza Jev e senza prova di Euclide I.10.

## Ipotesi

La tensione analogica iniziale fra i macrodomini ANGLES e SIDES precede e **co-determina quali sotto-Gestalten vengono cercate**. Costruire la bisettrice CD rende disponibili, dal basso, due settori angolari, porzioni della base, due triangoli e un carrier condiviso. Dal livello macro, l'attivazione delle opposizioni visive angolo↔lato e delle triplette lato–angolo–lato favorisce alcuni codelets. I nuovi raggruppamenti, a loro volta, possono riattivare le organizzazioni macro che li hanno favoriti.

Il ciclo va in **entrambe le direzioni**, non in stadi rigidi: la ricerca dell'analogia partecipa alla costruzione dei gruppi; i nuovi gruppi cambiano ciò che viene cercato.

Tensione orientata: dalla relazione data ∠ACD = ∠DCB alla possibile uguaglianza AD = DB?, passando per le opposizioni (∠ACD, AD) e (∠DCB, DB). **Questa tensione non è inferenza matematica**. Una bisettrice in un triangolo scaleno non è una mediana.

## Fonti reali del repository

- NMerovingio/graph/examples/generic_spaces_v0_8.json: fonte per i punti e i Mental Spaces MS_INITIAL_ANGLE, MS_INITIAL_SIDE, MS_LEFT, MS_RIGHT e gli schemi GS_SIDE_ANGLE, GS_MULTIPLE_ROLE.
- NMerovingio/graph/generic_space_memory_v0_9.json: schema storico GS_HIST_DOUBLE_TRIANGLE.
- Il medesimo CD conserva un'identità materiale fra le sue diverse partecipazioni. La costruzione scalena fa incontrare la bisettrice con AB secondo il rapporto AC:BC, non necessariamente nel punto medio.

## Meccanica sperimentale

1. CD crea nuove possibilità bottom-up; la costruzione garantisce solo l'uguaglianza dei due settori angolari.
2. Una Slipnet minimale contiene attivazioni di angles, sides, opposition, divider, sas, carrier.
3. I codelets ricevono un punteggio di affordance bottom-up e, nelle condizioni abilitate, un contributo da macro-tensione che privilegia il bridging angoli/lati.
4. Una softmax con temperatura (HEAT) sceglie quale codelet eseguire. **Temperatura e attivazione sono variabili diverse**: la prima regola la variabilità della scelta; la seconda trasporta la salienza.
5. Nella condizione reciproca, l'esecuzione di un codelet restituisce attivazione alla Slipnet: micro→macro.
6. La traccia di ogni evento conserva candidate scores, precondizioni, macro activation prima/dopo, temperature, eredità macro, descrizione, catena causale ed epistemic status.

## Tre condizioni, due geometrie

A. bottom_up: competizione fra codelets materialmente disponibili, senza pressione macro ereditata.

B. top_down: pressione iniziale macro angoli↔lati, senza feedback micro→macro.

C. reciprocal: stessa pressione macro iniziale più retroazione dai raggruppamenti attivati.

Stesso budget, stessi candidati, stesse geometrie e seed per ogni ablation. Due triangoli: isoscele e scaleno (controllo negativo).

Metriche: opposizioni visuali formate, triplette SAS riconosciute, proiezione della relazione angolare sul target segmentale ancora ipotetico, conteggio dei Generic Spaces candidati, primo tick della scoperta, eredità macro, eventi di feedback, false certificazioni metriche (devono restare ZERO).

## Riprodurre da root

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v1 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v1/engine.py --seeds 48 --budget 12
    python NMerovingio/experiments/gestalt_heat_v1/viewer.py

Aprire il file generato NMerovingio/experiments/gestalt_heat_v1/results/viewer.html. Confrontare condizioni, triangoli, seed e tick. REPORT.md sintetizza i risultati reali e traces.json ne conserva la genealogia.

## Limiti

Questo esperimento misura un meccanismo **progettato manualmente**; l'orientamento dato alla propagazione top-down è un'ipotesi implementativa. Un vantaggio nei benchmark non dimostra che Euclide o gli esseri umani ragionino in questo modo. Inoltre le partizioni candidate sono state enumerate in partenza: l'emergenza è una selezione e combinazione di codelets e non ancora generazione libera di nuove Gestalten dal grafo. Un esperimento successivo dovrà rimuovere il catalogo preenumerato, apprendere gli operatori e confrontare interventi causali selettivi sulle associazioni.
