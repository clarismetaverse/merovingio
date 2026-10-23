# Pertinenza dei bridge verificati: prima prova del ruolo JEV

Nel campione provato JEV mette al primo posto il bridge pertinente in tutte le sei graduatorie, senza pareggi. Ogni bridge riceve un punteggio più alto con il proprio obiettivo che con gli altri due, mantenendo identici candidati, immagini, certificati e domande. È un segnale favorevole al ruolo di valutatore di pertinenza su ipotesi già verificate dal codice, entro un obiettivo strutturale esplicito e semplice.

Fonte: [Actions 39938696779](https://github.com/clarismetaverse/merovingio/actions/runs/39938696779), commit live `bdc8099061e22f0822577182903dfbe6aafb9c2b`, branch `codex/verified-bridge-relevance`. Completati 99 test offline, build standard del viewer, sei richieste Jev 1.14.0 e audit in pipeline. Tutte le risposte dichiarano il modello richiesto. Nessun errore API, retry o seconda valutazione per correggere i risultati.

## Compito e distribuzione delle responsabilità

Tre tagli di un triangolo scaleno, ciascuno da un vertice a un punto interno del lato opposto. Tutti producono due triangoli adiacenti, con un solo carrier materiale comune, che partizionano l'ospite. Prima della chiamata il verificatore controlla identità, uso completo dei bordi, tipi, contenimento, disgiunzione degli interni e conservazione dell'area. Tutti i candidati soddisfano entrambi i contratti locali dei Generic Spaces storici GS_HIST_DOUBLE_TRIANGLE e GS_HIST_MEDIAL_POLYROLE.

Lo state espone certificati e relazioni strutturali dirette per tutti: vertice il cui fan è diviso, lato originario che riceve il contatto interno, nuovo carrier, regioni e ospite. Questo è un aiuto intenzionale: il recupero dal grafo e la correttezza del binding sono affidati al codice. Non sono forniti punteggi di riferimento, graduatorie, flag di corrispondenza con l'obiettivo o etichette del vincitore.

L'obiettivo cambia fra tre coppie di Mental Spaces: fan di un vertice e lato opposto, da confrontare tramite le due sottofigure e il nuovo carrier comune. La validità resta identica; cambia la pertinenza. Si ripete con una rotazione di 37 gradi e riflessione, nuovi alias e ordine dei candidati. Sono due presentazioni dello stesso triangolo, non due geometrie indipendenti.

Per candidato sono richiesti due Score nativi con quattro livelli descrittivi: accoppiamento dei Mental Spaces attivi e utilità dei Generic Spaces certificati per organizzare il confronto richiesto. Tre candidati per due dimensioni danno sei domande per richiesta; sei richieste producono 36 risposte. I due assi sono correlati. Il [Score nativo](https://docs.typesafe.ai/primitives/score) è conservato e diviso per tre; il composito usa pesi prefissati 0,5/0,5 in codice, secondo il [pattern ufficiale](https://docs.typesafe.ai/patterns/composite-scoring). Non è una probabilità di utilità.

## Risultati osservati

| Misura | Risultato |
| --- | ---: |
| Primo posto unico coerente con l'obiettivo | 6/6 |
| Confronti col riferimento superiore a ciascuna alternativa | 12/12 |
| Pareggi fra riferimento e alternative | 0 |
| Stesso bridge con score maggiore per il proprio obiettivo | 6/6 |
| Primo posto corretto sul solo asse Mental Spaces | 6/6 |
| Primo posto corretto sul solo asse Generic Spaces | 6/6 |

I nomi dei vertici sotto sono quelli visibili nelle immagini; gli alias dei candidati cambiano fra presentazioni. Punteggi compositi normalizzati 0–1, arrotondati qui a tre decimali e conservati integralmente nei dati.

| Presentazione | Fan attivo | Bridge primo | Score | Migliore alternativa | Margine |
| --- | --- | --- | ---: | ---: | ---: |
| Originale | D | C897 | 0,708 | 0,600 | 0,108 |
| Originale | E | C646 | 0,898 | 0,480 | 0,418 |
| Originale | A | C306 | 0,910 | 0,525 | 0,385 |
| Ruotata/riflessa | D | C176 | 0,933 | 0,537 | 0,397 |
| Ruotata/riflessa | E | C843 | 0,747 | 0,587 | 0,160 |
| Ruotata/riflessa | C | C415 | 0,845 | 0,502 | 0,343 |

Una preferenza fissa per un candidato o una posizione avrebbe coinciso con il riferimento in due casi su sei. Qui il primo posto cambia con l'obiettivo in entrambe le presentazioni. Inoltre, per ciascuno dei sei bridge osservati fra le due presentazioni, lo score con il proprio obiettivo supera entrambi gli score ottenuti con gli altri obiettivi: margini da 0,228 a 0,400. Questo è il controllo più diretto contro il semplice premio alla validità formale o a un candidato sempre favorito.

Entrambi gli assi separano il riferimento dalle alternative in ogni graduatoria: il risultato non dipende da una compensazione fra assi tramite il peso scelto. Non sono stati cercati pesi alternativi. Gli score assoluti variano fra presentazioni: non sono calibrati per una soglia automatica di azione o una misura universale di qualità.

## Cosa autorizza a concludere

In questa prova JEV distingue una costruzione pertinente da costruzioni ugualmente ammissibili rispetto a uno scopo esplicito. Il dato sostiene una pipeline in cui il codice produce e controlla i binding, poi JEV ordina un piccolo insieme in base allo scopo. I fallimenti dei precedenti test di binding restano tali; questo risultato non li corregge e non misura causalmente il vantaggio dei certificati, perché mancano qui un braccio senza certificati e il medesimo compito Choice.

La pertinenza è definita da un obiettivo geometrico poco ambiguo, i fatti utili sono esplicitati e il riferimento può essere ricavato dal codice. Non abbiamo misurato utilità matematica aperta, creatività, scoperta autonoma di obiettivi o Generic Spaces, generalizzazione a Euclide, estrazione dai soli pixel o prova geometrica. La componente di prioritizzazione compariva già nel precedente prototipo native-score: questa è una prova più circoscritta del ruolo con validità e pertinenza separate. Le sei graduatorie riusano la stessa figura e prompt correlati; non vanno trattate come sei campioni indipendenti per una stima generale di accuratezza.

Un seguito utile sarebbe fissare pochi obiettivi più ambigui e valutazioni di utilità indipendenti dai semplici criteri d'incidenza, includendo esplicitamente pareggi o più bridge utili. Non è stato eseguito in questa prova.

## Usage, affidabilità e conservazione

Usage dichiarato: 27.624 token input e 600 output, 4.604 input e 100 output per richiesta. Confidenza media 0,426, con 0,390 sull'asse Mental Spaces e 0,461 sull'asse Generic Spaces. La confidenza non è la correttezza della graduatoria. Affidabilità numerica e total_tokens non forniti, conservati null. Le probabilità ricevute sommano a uno; la massima discrepanza fra score nativo e attesa delle probabilità arrotondate è 0,03, mantenuta senza sostituire o rinormalizzare il risultato.

Ricostruiti gli hash di tutte le sei richieste e verificati tutti gli asset, le 36 risposte Score, i 36 controlli di contratto ripetuti sui candidati e i due gruppi di controfattuali in cui cambia soltanto active_objective. Ricalcolate tutte le graduatorie, i margini e i cambi d'obiettivo. Il viewer e il pacchetto contengono score separati, immagini, dati sanitizzati, protocollo, certificati, provenienza storica e audit. I numeri nativi sono riportati prima di qualsiasi interpretazione.

Live soltanto GitHub Actions, con TYPESAFE_API_KEY secret e TypeSafe-Danger-Zone-Images: true. Nessun long context, chiave esposta o risposta grezza del server negli errori. Main e lavoro v0.9/v1.0 preservati sul branch dedicato. Le immagini mostrano alternative prospettiche: non sono una sequenza temporale e non attestano ragionamento sequenziale interno.
