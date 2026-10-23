# Merovingio v4 — REBASE ricorsivo esclusivamente delle opposizioni lato–angolo

## Ipotesi cognitiva

La costruzione CD induce più organizzazioni simultanee della figura, legate dalla genealogia dello stesso carrier materiale e dal punto d'incidenza. Su questa base, la tensione analogica angoli↔lati può **far rileggere ripetutamente** lo stesso sistema di opposizioni: ogni REBASE porta in primo piano l'altro dominio e importa un NUOVO witness strutturale, preservando quelli già acquisiti.

Quindi non è una semplice inversione logica delle premesse, né un ping-pong fra etichette. È uno spostamento del fuoco che produce una rappresentazione cumulativamente più ricca.

### Ciclo atteso, non preimpostato come un ordine di dimostrazione

Un possibile percorso:

1. Focalizzazione iniziale sui due angoli (con uguaglianza data se CD è bisettrice).
2. REBASE ANGLE→SIDE: rilettura di AD/DB come porzioni della stessa base, con opposizioni fra coppie di angoli e lati.
3. REBASE SIDE→ANGLE: ritorno agli angoli, aggiungendo la partizione angolare o il raggio comune.
4. REBASE ANGLE→SIDE: nuova lettura dei segmenti attraverso il punto comune d'incidenza D.
5. REBASE SIDE→ANGLE: nuova interpretazione degli angoli attraverso il medesimo CD.

L'ordine e la lunghezza dipendono dalle scelte stocastiche. Ogni interpretazione aggiunge evidenza letta da relazioni reali del grafo (PART_OF, BOUNDS_ANGLE, ENDPOINT, GIVEN_EQUAL), e il ciclo si arresta quando non esistono più supporti nuovi nel dominio di destinazione.

NON ci sono REBASE di triangoli o altri domini. I triangoli preesistono come regioni nel grafo materiale, ma non diventano un oggetto di rebase, e non si usa SAS/LLL per produrre un'uguaglianza.

### Direzionalità dell'analogia e relazione metrica

Se la bisettrice garantisce ∠ACD=∠DCB, la prima rilettura ANGLE→SIDE può proporre la DOMANDA AD=DB?. Questa è un'ipotesi di trasferimento attraverso due opposizioni angolo–lato, non una proposizione dimostrata e non una misura. Nel triangolo scaleno la domanda rimane generalmente falsa. Nel controllo con una trasversale ordinaria non esiste l'uguaglianza angolare sorgente e NON viene posta quella domanda.

La direzione SIDE→ANGLE rilegge relazioni strutturali; NON assume che i lati siano uguali e non genera un converso metrico fittizio.

### Attivazione e heat

La macro-attivazione nei concetti angles, sides, opposition e coorigin è separata da una temperatura stocastica. Il termine medio CD fa da ancoraggio genealogico. Ogni nuovo REBASE può modificare localmente le attivazioni quando il feedback è abilitato.

Confrontiamo le condizioni:

- no_pressure: sola disponibilità dei witness sul grafo, nessuna attivazione macro.
- macro_only: attivazione macroscopica lato/angolo/opposizione senza prior genealogica né feedback.
- genealogy_only: salienza dovuta alla co-origine senza macro-opposizione.
- recursive_coupled: entrambe le pressioni + feedback bidirezionale.
- recursive_genealogy_blind: macro-opposizione + feedback, ma genealogia oscurata nello score.
- one_way: come la condizione completa, ma consente soltanto ANGLE→SIDE e non il ritorno.

Il grafo e il sistema di opposizioni sono identici nelle condizioni per ciascuna geometria. Cambiano solo le priorità cognitive o il permesso del REBASE inverso.

### Metriche

Numero REBASE, probabilità che il loop ritorni ad un dominio già visto con un NUOVO witness, supporti distinti incorporati, domande analogiche generate, REBASE ridondanti (0 per costruzione, testato), asserzioni metriche illegittime (0 per costruzione, testato).

Questa è una simulazione con prior e regole di aggiornamento manuali: validiamo l'operatore nel software, non una teoria sperimentale dei ragionamenti storici o umani.

## Esecuzione

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v4 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v4/rebase_loop.py --seeds 48 --budget 8
    python NMerovingio/experiments/gestalt_heat_v4/viewer.py

Artefatti: results/traces.json, results/aggregates.json, results/REPORT.md, results/viewer.html.

Fonti geometriche: v3 poristic.py e v2 endogenous.py; ontologia e memoria nei fixture NMerovingio/graph.
