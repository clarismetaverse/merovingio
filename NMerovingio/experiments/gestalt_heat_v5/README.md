# Merovingio v5 — Dynamic Opposition REBASE (solo angoli ↔ lati)

## Domanda

Nella v4 il motore alternava Angular Space e Side Space leggendo un elenco fisso di witness. La v5 mantiene il solo REBASE delle **opposizioni angolo–lato** ma lascia che **ogni nuovo gruppo modifichi la salienza di tutte le opposizioni ancora disponibili**.

La figura non è reinterpretata secondo una sequenza preimpostata di risultati: per ciascun REBASE, il sistema ricalcola la probabilità di tutti i successivi mapping oppositivi estratti dal grafo. Il ramo rimane radicato nella costruzione CD.

## Rappresentazione

- Il grafo materiale ricava angoli, segmenti e relazioni di opposizione dai triangoli. Le coppie non sono hard-coded come AD↔∠ACD.
- Le due partizioni della stessa costruzione sono associate a un registro di co-origine (coorigin ledger), separato dalle relazioni metriche.
- Ogni candidato REBASE è una relazione angolo opposto a segmento. Il dominio cambia ANGLE→SIDE o SIDE→ANGLE, ma l'opposizione particolare è ricalcolata dinamicamente.
- Dopo ogni selezione, l'attivazione dei due oggetti viene propagata lungo le relazioni endpoint, part_of, bounds_angle, opposite, boundary e angle_in_region. Nel caso di genealogia condivisa si propaga anche alle due partizioni generate dallo stesso carrier.
- I macroconcetti angles, sides, opposition, coorigin possono biasare la scelta e ricevere retroazione.
- Quando due opposizioni esplorate condividono un contesto strutturale, emerge un Generic Space candidato con provenance e supporti.
- Quando emergono le opposizioni dei due angoli dati uguali, il REBASE può proporre la domanda AD = DB?; **non la certifica**. Nel caso scaleno tale uguaglianza in generale è falsa. La trasversale arbitraria non porta neppure il dato sorgente di uguaglianza angolare.

## Ablazioni

| Condizione | Ranking aggiornato | Campo locale | Macro | Genealogia | Feedback macro |
|---|---|---|---|---|---|
| fixed_order | No | No | Iniziale | Statica | No |
| local_only | Sì | Sì | No | Locale | No |
| macro_no_feedback | Sì | Sì | Sì | Sì | No |
| macro_no_genealogy | Sì | Sì | Sì | No | Sì |
| coupled | Sì | Sì | Sì | Sì | Sì |

Le condizioni condividono geometria, candidati, budget e seed.

## Test

- La propagazione di un raggruppamento deve modificare la salienza relativa delle alternative, non distribuire lo stesso bonus a tutte.
- Tracciamo ranking prima e dopo, attivazioni locali, partecipazioni del carrier e nuovi Generic Spaces.
- Il controllo fixed_order non cambia ranking sulla base dell'evidenza appena acquisita.
- Nessuna coppia di opposizione viene ripetuta: la ricorsione produce nuove letture, non una semplice alternanza verbale.
- Nessuna tensione analogica viene promossa a uguaglianza metrica verificata.

## Limiti

Modello ingegnerizzato: gli operatori, i pesi e la diffusione sono progettati manualmente, non appresi, e i Generic Spaces sono strutture candidate. Non è un test della cognizione umana né una prova euclidea. Il modello non costruisce nuove figure e non fa REBASE tra triangoli.

## Esecuzione dalla root

    python -m unittest discover -s NMerovingio/experiments/gestalt_heat_v5 -p 'test_*.py' -v
    python NMerovingio/experiments/gestalt_heat_v5/dynamic.py --seeds 32 --budget 4
    python NMerovingio/experiments/gestalt_heat_v5/dynamic.py --seeds 32 --budget 8 --output NMerovingio/experiments/gestalt_heat_v5/results/saturation
    python NMerovingio/experiments/gestalt_heat_v5/viewer.py

Aprire results/viewer.html, confrontare le condizioni ed esaminare results/traces.json.

## Primary evaluation vs saturation

Il benchmark principale limita la ricerca a QUATTRO REBASE su più opposizioni, per misurare quali alternative vengono esplorate; il controllo di saturazione ammette OTTO passi, quasi esaurendo le opzioni. Un ranking fisso ben inizializzato può legittimamente superare la ricerca dinamica: non considerare le frequenze di Generic Spaces o i riordinamenti come misure autonome di reasoning. Il file SATURATION_COMPARISON.md mette a confronto i due orizzonti.
