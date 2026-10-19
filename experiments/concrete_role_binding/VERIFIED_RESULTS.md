# Binding concreto e controesempi vicini

Il contratto esplicito non basta a garantire che Jev segua correttamente i riferimenti agli oggetti. Nel formato provato, seleziona il witness corretto in tutti gli otto casi base, ma accetta un'assegnazione materialmente errata in tutti gli otto controesempi con carrier coincidenti e identità distinte. Sbaglia anche tutti gli otto casi in cui il witness corretto è stato tolto dalle opzioni.

La valutazione verificata è il [run Actions 39228730075](https://github.com/clarismetaverse/merovingio/actions/runs/39228730075), commit `3a44de298fd449c2dc01da98b0600e94b6f5e516`, branch `codex/concrete-binding-near-misses`, discendente dagli esperimenti precedenti. Completati 69 test offline, build e quattro chiamate live Jev 1.14.0, senza errori API. Ogni chiamata contiene dodici Choice: 48 risposte in totale. Main, v0.9/v1.0 e risultati precedenti restano preservati.

## Che cosa è stato chiesto

Per due schemi storici operazionalizzati, Jev sceglie fra cinque assegnazioni di carrier, coppia di regioni e figura ospite, oppure none. Tutti gli oggetti proposti hanno il tipo giusto. Il modello deve distinguere identità materiale, uso completo di un lato, regione coincidente ma diversa, adiacenza, contenimento e partizione dell'intera figura ospite. Il witness è fornito come candidato typed: la prova misura selezione fra assegnazioni, non generazione libera di un binding.

Lo state contiene oggetti, coordinate, cicli di vertici e riferimenti degli usi di bordo. Gli ID sono locali allo snapshot e definiscono l'identità materiale nel contratto di questa prova; coordinate uguali non fondono oggetti distinti. Le immagini non hanno etichette o risposte. Quattro repliche cambiano ID, ordine delle opzioni/domande, rotazioni e riflessioni. Sono pochi template sintetici trasformati, non 48 geometrie indipendenti o un campione dell'intero corpus di Euclide.

## Risultati nativi prima di ogni gate

| Controllo | Risposte esatte | Dettaglio |
| --- | ---: | --- |
| Caso base condiviso | 8/8 | Carrier, regioni e host selezionati correttamente |
| Carrier coincidenti ma distinti | 0/8 | Accettati witness che violano l'identità materiale |
| Uso parziale del carrier | 4/8 | Quattro rifiuti corretti; quattro accettazioni invalide |
| Triangolo più quadrilatero | 3/8 | Due rifiuti corretti per il doppio triangolo e un binding polyrole corretto |
| Figura ospite diversa | 4/8 | Un binding di contenimento corretto e tre rifiuti di partizione corretti |
| Witness corretto escluso dalle opzioni | 0/8 | Scelte assegnazioni invalide invece di none |

Complessivamente: **19/48 risposte esatte**. Su sedici domande con un witness valido fra le opzioni, dieci assegnazioni corrette e sei false astensioni. Su trentadue domande senza witness valido fra le opzioni, nove none corretti e ventitré assegnazioni invalide accettate. Rispondere sempre none darebbe 32/48: l'accuratezza aggregata da sola sarebbe fuorviante. La coppia caso base più controesempio di identità è interamente corretta in zero casi su otto.

| Riferimento | Witness valido scelto | Witness errato scelto | none |
| --- | ---: | ---: | ---: |
| Witness valido presente | 10 | 0 | 6 |
| Nessun witness valido presente | 0 | 23 | 9 |

## Il controesempio più informativo

Nel caso base due regioni adiacenti usano lo stesso segmento S come lato completo. Nel controfattuale cambia un solo riferimento: il bordo della seconda regione usa T, un segmento distinto con gli stessi endpoint e le stesse coordinate. Il resto del grafo è identico e viene riutilizzato lo stesso asset immagine, pixel per pixel. Non esiste più il carrier materiale comune richiesto dal contratto.

Jev continua a selezionare un witness basato su S, T oppure su una regione coincidente che usa un terzo carrier. Tutte queste scelte sono invalide nel grafo dichiarato. Negli otto casi con witness corretto omesso, sceglie analogamente segmenti o regioni vicini ma con incidenze materiali incompatibili. Questi sedici errori di identità spiegano sedici delle ventitré accettazioni invalide.

Gli altri errori selezionati violano uso completo del carrier, tipo delle regioni o copertura della figura ospite. Le categorie di violazione possono sovrapporsi: quattro scelte hanno uso incompleto del lato, tre partizione incompleta dell'host e due tipi di regione incompatibili. La figura ospite esterna contiene la coppia di triangoli, quindi ammette il primo schema, ma non è interamente coperta e quindi non ammette il polyrole di partizione. Jev rifiuta anche tre dei quattro binding di contenimento validi in questo controllo.

## Come leggere il risultato rispetto alla prova precedente

Il precedente recupero di 28/28 dimostrava che una descrizione esplicita rendeva riconoscibile il significato operativo generale dello schema su quelle fixture. Non dimostrava ancora l'affidabilità del binding puntuale fra ruoli e ID. Questa prova aggiunge oggetti coincidenti, assegnazioni alternative molto vicine e witness mancanti, ed evidenzia quel limite.

Il fallimento riguarda il formato multimodale e strutturato testato. Non isola una causa interna al modello e non distingue ancora costo del contesto, formato dei riferimenti e uso delle immagini. La geometria strutturata era fornita, quindi il risultato non può essere spiegato semplicemente come difficoltà di riconoscimento visivo. Il benchmark usa una politica locale di identità per ID e un verificatore di poligoni convessi, non una certificazione dell'intero motore di Merovingio o della sua ontologia.

## Conseguenza pratica

Conservare la proposta Jev e verificare in codice gli ID effettivi, le incidenze, l'estensione dell'uso di bordo e la figura ospite prima di accettare il binding. Il verificatore respingerebbe le ventitré assegnazioni invalide osservate; questo è un risultato del controllo deterministico, non un miglioramento delle risposte native di Jev. I sei witness validi mancati dal modello rimangono mancati. Non viene applicata una correzione a posteriori ai conteggi 19/48.

Il codice sperimentale espone check_witness e all_bindings come controlli locali riproducibili. Non è stato cambiato il motore applicativo o riscritta la memoria storica. Una diagnosi ulteriore potrebbe confrontare contesto completo e una piccola tabella delle sole incidenze rilevanti; non sono state aggiunte chiamate oltre le quattro previste.

## Audit e conservazione

Ricostruiti tutti e quattro gli hash delle richieste dagli input e dalle immagini scaricate; verificati i 48 output typed, tutte le 240 assegnazioni offerte, le quattro mutazioni di un solo campo con immagine identica e le matrici. Il verificatore controlla identità degli oggetti e uso completo, intersezioni con clipping convesso, contenimento e aree. Una tolleranza di 1e-4 sulle quantità geometriche assorbe l'arrotondamento delle rotazioni; i test confermano invarianti le etichette di riferimento nelle quattro trasformazioni.

Usage dichiarato: 59.040 token input e 3.663 output; total_tokens non fornito. Confidenza media dichiarata 0,54625. Affidabilità numerica non fornita, conservata come null. Le probabilità native arrotondate hanno scarto massimo dalla somma uno di 0,01 e sono conservate senza rinormalizzazione. La confidenza non viene interpretata come garanzia di correttezza.

Live solo su GitHub Actions con TYPESAFE_API_KEY secret e TypeSafe-Danger-Zone-Images: true. Nessuna chiave, corpo di errore grezzo, retry o long context. Artifact, immagini, risposte sanitizzate, input ricostruibili, viewer offline e matrici sono salvati in outputs e Library. Gli snapshot sono alternative controfattuali, non frame temporali: più immagini non dimostrano ragionamento sequenziale interno, prova geometrica o estrazione autonoma di tutte le relazioni.
