# Scoring nativo Jev su un workspace condiviso

Il prototipo usa lo scoring nativo di Jev 1.14 per valutare bridge rispetto a Mental Spaces e Generic Spaces e per vagliare schemi candidati. `state` rappresenta il workspace condiviso: figura, oggetti, immagini, spazi esistenti e trasformazioni ipotetiche. Le domande interrogano quel workspace in parallelo. Il codice combina gli score, applica i profili di priorità e verifica i binding. Questo non implica memoria persistente fra chiamate, scoperta autonoma di schemi o prova geometrica.

La prova verificata è il [run GitHub Actions 39216941401](https://github.com/clarismetaverse/merovingio/actions/runs/39216941401), commit `1cf3919c0d98021c62c5e85f85f5b4b2b4e51909`, branch `codex/native-score-bridge-generic-search`. Completati 49 test offline, build del viewer esistente e valutazione live: 8 chiamate riuscite, 432 risposte native Score, nessun errore API. Main rimane `7ec0c2b8e7a4f0e0cac82a1265a53e3fb5a98475`; la storia sperimentale v0.9/v1.0 e i quattro benchmark temporali sono preservati.

## Dimensione del confronto

Due triangoli scaleni, due ripetizioni con etichette anonime e ordine modificati, cinque bridge ipotetici inclusa una trasformazione nulla. Le immagini sono accompagnate da geometria strutturata estratta dal codice: la prova non misura estrazione visiva autonoma.

Il repository contiene dieci Generic Spaces e cinque record di proposizioni, non l'intero corpus di Euclide. I dieci schemi sono affiancati da due proposte generate dal codice: interfaccia condivisa e coppia congruente. Le dodici descrizioni model-visible sono distinte e conservano le premesse semantiche dei record, senza identificativi delle fonti. Jev valuta ipotesi fornite, non inventa liberamente queste proposte.

Il batch ridotto contiene 40 domande per cinque bridge su otto dimensioni MS/GS e 60 domande di compatibilità, una per ogni coppia bridge-schema. Sono 100 domande, non 100 teoremi. I quesiti locali più dettagliati non vengono chiamati in questo pilot. Il controllo usa otto domande identiche estratte dal batch completo, con stesso state e stesse immagini.

| Misura media su quattro coppie | 8 domande | 100 domande |
| --- | ---: | ---: |
| Tempo HTTP compresa lettura e sanitizzazione | 0,170 s | 0,380 s |
| Mediana del tempo | 0,163 s | 0,392 s |
| Token input dichiarati dall'API | 12.246,5 | 44.641,5 |

Il tempo medio cresce di circa 2,23 volte e i token di 3,65 volte, con 12,5 volte le domande. Sono quattro coppie seriali con ordine controbilanciato: descrivono questa prova e non garantiscono latenza costante a 200 o 2000 schemi. Sui 32 score sovrapposti, la variazione assoluta media normalizzata fra batch piccolo e grande è 0,006875: i risultati non sono perfettamente invarianti alla composizione del batch.

## Ranking dei bridge

Gli score nativi hanno quattro livelli descrittivi, da 0 a 3. Il codice divide per 3 e applica pesi dichiarati prima della prova. Un profilo privilegia il ventaglio in C e il lato AB, l'altro il ventaglio in A e il lato BC. I pesi e il riferimento indipendente non sono inviati a Jev.

Il bridge preferito dal riferimento è primo e selezionato in tutti gli otto confronti: quattro con priorità C e quattro con priorità A. Il risultato mostra riuso degli stessi score per obiettivi diversi su due fixture, non una misura universale di qualità o creatività geometrica.

## Selezione dei Generic Spaces

La soglia normalizzata di screening, fissata prima della prova, è 0,75. Il confronto seguente riguarda 240 coppie bridge-schema e usa il controllo strutturale locale come riferimento; non valuta la validità universale dei teoremi.

| Screening Jev | Binding previsto dal controllo | Binding non previsto |
| --- | ---: | ---: |
| Sopra soglia | 16 | 0 |
| Sotto soglia | 28 | 196 |

Tutti i 16 binding sopra soglia riguardano la proposta di interfaccia condivisa. Il modello mantiene sotto soglia 28 binding dei due schemi storici compatibili con il controllo locale. Lo screening ampio è quindi conservativo: non va descritto come selezione completa dei Generic Spaces esistenti. Il viewer mostra anche questi mancati riconoscimenti, anziché nasconderli con i controlli del codice. La precisione osservata dopo un gate non sarebbe una capacità aggiuntiva di Jev.

Nessuna coppia congruente è accettata; le regioni hanno aree diverse e manca una certificazione di congruenza. Le memorie di proposizione restano template condizionali: mancanza di premesse certificate nel workspace non equivale a confutazione del teorema.

## Tracciabilità e limiti

Usage complessivo dichiarato: 227.552 token input e 7.376 output. Il campo total_tokens non è fornito; non viene inventato. Confidenza media dichiarata 0,7922; affidabilità numerica assente, conservata come null. Le probabilità native arrotondate hanno deviazione massima dalla somma uno di 0,01 e discrepanza massima fra score nativo e valore atteso delle probabilità di 0,03. Restano inalterate nei risultati.

L'audit ricostruisce le otto richieste dalle immagini e dagli input sanitizzati, verifica tutte le impronte, i quattro workspace condivisi, i 432 score normalizzati e ricalcola ranking e gate. Le piccole differenze di somma floating-point fra versioni Python sono controllate con tolleranza 1e-12. Le chiavi non sono salvate. Le chiamate avvengono solo in Actions con secret e header immagini richiesto; long context è disattivato.

I tentativi da 220 domande restituiscono HTTP 400 con indicatore diagnostico legato ai token e sono archiviati separatamente. Il primo run da 100 domande, 39216690245, è completato ma superato per confronti fra schemi: cinque descrizioni di proposizioni erano state rese identiche dalla proiezione. Il run verificato ripristina le premesse e aggiunge un controllo di unicità. Nessuno di questi tentativi è nascosto o contato tra le otto chiamate della misura finale.

Per estendere il corpus, usare uno score sintetico per schema in batch che rispettino il budget e approfondire i candidati rilevanti. Non moltiplicare automaticamente ogni teorema per ogni dimensione. I limiti documentati sono 64k per richiesta e 32k per state più singola domanda, senza tetto separato al numero di domande. La condivisione del workspace risparmia ripetizioni; domande e schemi continuano ad aggiungere token. [Modelli e limiti TypeSafe](https://docs.typesafe.ai/models), [fan-out](https://docs.typesafe.ai/patterns/fan-out), [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).

I risultati precedenti sulle sequenze restano separati: più immagini in input non dimostrano ragionamento sequenziale interno. La distinzione `SAME_FINAL_STATE != SAME_GENEALOGY` rimane valida; questa prova studia selezione di trasformazioni strutturali su un workspace, non equivalenza tra genealogie o prova geometrica.
