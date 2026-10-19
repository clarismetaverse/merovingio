# Perché mancavano i binding dei Generic Spaces storici

Su questi quattro workspace, il principale ostacolo è la descrizione astratta dello schema nello state e il suo allineamento al significato operativo del binding. Rendendo espliciti i ruoli richiesti, Jev recupera tutti i 28 binding anche mantenendo gli stessi criteri generici e la stessa soglia di prima. Criteri più concreti aiutano, ma da soli recuperano soltanto i 12 binding del doppio triangolo. Cambiare soltanto il tipo di risposta o abbassare la soglia non risolve entrambi gli schemi.

La valutazione verificata è il [run GitHub Actions 39220562883](https://github.com/clarismetaverse/merovingio/actions/runs/39220562883), commit `951dadb81197a67750020a16d03a9aad1b562d26`, branch `codex/generic-binding-description-scoring`, discendente dalla precedente prova verificata. Completati 59 test offline, build e 16 chiamate live, senza errori API: 320 risposte native, 160 Score e 160 Choice. Ogni chiamata contiene soltanto 20 domande; le valutazioni richieste scendono rispetto alle 432 della prova precedente. Anche i token input scendono, da 227.552 a 166.688. Le immagini e i workspace precedenti rimangono conservati; main non viene modificato.

## Il confronto che separa le due ipotesi

Il confronto riguarda soltanto i due schemi storici che avevano prodotto i 28 mancati riconoscimenti. Si mantengono i quattro workspace originali, con cinque candidati ciascuno e i controlli negativi: 28 binding attesi e 12 non attesi. Sono due template geometrici con ripetizioni di etichetta e ordine, non 28 geometrie indipendenti.

| Descrizione nello state | Criteri | Score con soglia 0,75 | Choice, livello di binding completo | Falsi positivi Score / Choice |
| --- | --- | ---: | ---: | ---: |
| Compatta originale | Generici originali | 0/28 | 3/28 | 0/12 / 0/12 |
| Esplicita | Generici originali | 28/28 | 28/28 | 0/12 / 0/12 |
| Compatta originale | Concreti | 12/28 | 15/28 | 0/12 / 0/12 |
| Esplicita | Concreti | 28/28 | 28/28 | 0/12 / 0/12 |

Nella condizione compatta con criteri concreti, Choice risponde none su 13 binding positivi. Tutte le altre condizioni hanno zero none. Le matrici complete sono in results.json e nel viewer. I risultati non sono filtrati attraverso il gate prima di contarli: eventuali falsi positivi restano visibili.

La baseline compatta e generica nel batch ridotto continua a mancare tutti i 28 binding, come nel precedente batch da 100 domande. La variazione assoluta media dello score sui 40 confronti è 0,01608, senza recuperi sopra soglia. Il recupero nelle altre condizioni non si spiega quindi semplicemente con la riduzione del batch in questa prova.

## Che cosa è stato reso esplicito

La descrizione originaria del doppio triangolo conteneva relazioni come `same_material_carrier` e `both_participate_in_same_carrier`, con il vincolo di due regioni triangolari. La descrizione esplicita definisce un segmento materiale s e due regioni distinte R0/R1, e chiarisce che s è un lato completo di entrambe: identità dello stesso oggetto, non uguaglianza di lunghezza fra oggetti diversi. Non richiede congruenza o ulteriori premesse metriche.

Per il polyrole, `one_material_identity` e `distinct_participations` non specificavano da soli quali partecipazioni fossero richieste in questo test. La definizione esplicita distingue il ruolo di lato delle due regioni dal ruolo di partizione interna della figura ospite, sempre per lo stesso segmento. Le regioni non devono necessariamente essere entrambe triangoli.

Queste definizioni sono regole generiche e non contengono assegnazioni ai candidati, risposte attese, nuovi fatti geometrici o dichiarazioni che un binding sia presente. La geometria, le immagini, i nomi anonimi e tutti gli altri campi dello state restano uguali. Tuttavia chiariscono un significato operativo prima sottospecificato: il risultato dimostra sensibilità alla descrizione e alla sua corrispondenza col controllo locale, non che Jev avesse necessariamente frainteso un testo originario univoco. La memoria storica non viene riscritta retroattivamente.

## Quanto incidono i criteri e la soglia

A descrizione compatta invariata, i criteri concreti portano il doppio triangolo da 0/12 a 12/12, mentre il polyrole resta 0/16 sopra soglia. Il suo score medio positivo aumenta da 0,234 a 0,573: i criteri aiutano ma l'interpretazione del ruolo resta problematica. Esplicitando lo schema e mantenendo i criteri generici, i due score medi positivi arrivano rispettivamente a 0,892 e 0,882.

L'effetto medio appaiato della descrizione esplicita sui positivi è +0,485 con i criteri generici e +0,224 con quelli concreti. L'effetto dei criteri concreti è +0,353 con descrizione compatta e +0,092 con descrizione esplicita. Sono differenze descrittive sulle stesse fixture, senza inferenza statistica su un corpus più ampio.

La classe modale del medesimo Score riconosce 9/28 binding con descrizione compatta e criteri generici, e 24/28 con criteri concreti. Questo mostra che la riduzione dello score a una soglia perde parte dell'informazione della distribuzione; non recupera però tutti i binding e non sostituisce la necessità di una definizione chiara. Il valore Score è una posizione ordinale attesa, non la probabilità che il binding sia vero. [Semantica ufficiale di Score](https://docs.typesafe.ai/primitives/score).

Abbassare la soglia a 0,50 nella baseline recupera 12/28 binding ma introduce un falso positivo. Con descrizione compatta e criteri concreti, la stessa soglia recupera 25/28 introducendo quattro falsi positivi. Questi ultimi riguardano il doppio triangolo sul candidato che produce un triangolo e un quadrilatero: il supporto è parziale, non un binding completo. Le soglie 0,50, 0,65, 0,75 e 0,85 erano dichiarate prima della prova e sono solo diagnostiche. La soglia principale resta 0,75.

Choice riusa le identiche istruzioni e i quattro testi dei livelli, con etichette neutre randomizzate e un'opzione none aggiuntiva. Quindi il confronto fra primitive comprende anche una diversa possibilità di astensione. Il semplice passaggio a Choice nella baseline recupera soltanto 3/28 binding; con descrizioni esplicite, Score e Choice concordano su tutti i 40 casi. Non emerge un limite generale della primitiva Score da questa prova.

## Conseguenza pratica

Per lo screening dei Generic Spaces conviene fornire nello state un piccolo contratto di binding per ciascuno schema: tipi degli oggetti, relazioni richieste, identità materiale, partecipazioni distinte e stato delle eventuali premesse metriche. Il contratto deve dichiarare lo schema, senza assegnarlo in anticipo ai candidati. I criteri Score possono poi restare brevi e riferirsi a quel contratto; i gate strutturali indipendenti continuano a verificare il risultato.

Questa è una raccomandazione sostenuta dalle fixture attuali, non una soluzione già validata per tutti i Generic Spaces o per migliaia di teoremi. Le descrizioni esplicite sono salvate nel modulo sperimentale come EXPLANATIONS; la memoria v0.9 e i precedenti esperimenti restano intatti. Prima di trasferire la regola a un catalogo ampio servono schemi e geometrie non usati per questa diagnosi.

## Tracciabilità

Ricostruite tutte le 16 richieste e le quattro richieste originarie dalle immagini congelate e dagli input archiviati. Verificati tutti gli hash, le variazioni limitate alle definizioni/criteri, i 320 output typed, normalizzazione e statistiche. Usage dichiarato: 166.688 token input e 13.621 output; total_tokens non fornito. Confidenza media dichiarata 0,66053 sulle due primitive insieme; affidabilità numerica non fornita, conservata come null. Le probabilità arrotondate hanno deviazione massima dalla somma uno pari a 0,01 e sono preservate senza rinormalizzazione.

Solo Actions usa il secret TYPESAFE_API_KEY e l'header TypeSafe-Danger-Zone-Images: true; nessuna chiave o corpo di errore grezzo è salvato. Non si attiva long context. Il viewer funziona offline e mostra matrici, score per schema, none, soglie, input e risposte sanitizzate. La geometria strutturata resta evidenza fornita dal codice: questa prova non misura estrazione visiva autonoma, scoperta libera, validità di teoremi o ragionamento sequenziale interno.
