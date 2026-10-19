# State completo o sole incidenze rilevanti

La riduzione del contesto migliora soprattutto i rifiuti dei witness invalidi, ma non rende affidabile l'associazione dei ruoli agli ID. Sulle stesse 24 domande, le risposte esatte salgono da 8 a 12; i witness positivi corretti scendono da 5/8 a 4/8, mentre i none corretti salgono da 3/16 a 8/16. L'identità materiale resta problematica anche con il solo snapshot rilevante e tutti i dati necessari intatti.

La misura verificata è il [run GitHub Actions 39236636905](https://github.com/clarismetaverse/merovingio/actions/runs/39236636905), commit `03835dc062353ac4b55f5c1eb1826bc270d46f6c`, branch `codex/concrete-binding-reduced-state`. Completati 79 test offline, build e 24 chiamate live Jev 1.14.0 senza errori API: due domande per chiamata, 48 risposte native nel confronto finale. Main e gli esperimenti precedenti restano preservati.

## Confronto appaiato

Si riusano due repliche del benchmark precedente, tutti i sei casi e i due contratti, con ID, immagini, opzioni, ordine e istruzioni identici fra le condizioni. Lo state completo ha quattro snapshot e 112 oggetti. Quello ridotto ha un solo snapshot e 20–25 oggetti: si parte da TUTTE le opzioni offerte e si mantengono tutti gli oggetti raggiungibili, ogni uso di bordo, i carrier con endpoint, i poligoni e i punti. Non viene aggiunta alcuna spiegazione della risposta o nuovo fatto geometrico.

Il verificatore produce gli stessi motivi di invalidità per tutte le 240 assegnazioni offerte e trova gli stessi binding esistenti prima e dopo la riduzione. Anche i carrier coincidenti e le regioni ingannevoli restano presenti. Le coordinate sono conservate perché adiacenza, contenimento e copertura della figura ospite richiedono informazione geometrica oltre all'incidenza simbolica.

| Misura | State completo | State ridotto |
| --- | ---: | ---: |
| Risposte esatte | 8/24 | 12/24 |
| Witness positivi corretti | 5/8 | 4/8 |
| none corretti sui negativi | 3/16 | 8/16 |
| Witness invalidi accettati | 13 | 8 |
| False astensioni sui positivi | 3 | 4 |
| Dimensione media dello state JSON UTF-8 | 10.788 byte | 3.586 byte |
| Token input medi per chiamata | 12.755 | 5.682 |

Lo state testuale si riduce di circa il 67%; i token input dichiarati per chiamata di circa il 55%. Le immagini sono identiche e restano tutte disponibili in entrambe le condizioni. Rispondere sempre none produrrebbe 16/24: il risultato ridotto di 12/24 non è da presentare come una policy di binding riuscita.

| Caso | Completo | Ridotto |
| --- | ---: | ---: |
| Caso base con carrier condiviso | 4/4 | 4/4 |
| Carrier coincidenti ma materialmente distinti | 0/4 | 1/4 |
| Uso parziale del carrier | 1/4 | 3/4 |
| Triangolo più quadrilatero | 1/4 | 2/4 |
| Figura ospite diversa | 2/4 | 2/4 |
| Witness corretto escluso dalle opzioni | 0/4 | 0/4 |

Nel caso triangolo più quadrilatero il miglioramento aggregato nasconde uno scambio: i due negativi del doppio triangolo vengono rifiutati, ma entrambi i positivi polyrole sono mancati; nello state completo era riconosciuto uno dei due. Anche con contesto ridotto il modello manca entrambi i binding di semplice contenimento nella figura ospite esterna, pur rifiutando correttamente entrambi i binding che ne richiederebbero una partizione completa.

## Quanto pesa il contesto

Nei 24 confronti appaiati, sette risposte sono corrette in entrambe le condizioni, cinque migliorano con la riduzione, una peggiora e undici restano errate. La baseline completa ripetuta ottiene 8/24 contro 7/24 del sottoinsieme storico, con due scelte cambiate. Il confronto storico comprende cambio di batch, nuova esecuzione e aggiunta del manifest immagini comune; non isola separatamente questi effetti. Il confronto completo-ridotto della misura attuale mantiene invece lo stesso batch da due domande e lo stesso manifest.

Questi dati sostengono un contributo della rilevanza del contesto nel formato testato, soprattutto per non accettare supporto parziale come binding completo. Non sostengono che il problema fosse soltanto la quantità di contesto: tre dei quattro casi di identità distinta e tutti i quattro casi con witness corretto omesso restano errati, mentre la sensibilità sui positivi peggiora leggermente. La coppia base più controesempio di identità è interamente corretta in 0/4 casi con state completo e 1/4 con state ridotto.

La riduzione rimuove insieme snapshot concorrenti e oggetti non raggiungibili; non distingue i due contributi. Mantiene anche tutte le immagini originali. Un risultato parziale non esclude ulteriori effetti di rappresentazione o del contesto visivo, né dimostra un'incapacità generale o intrinseca di Jev di trattare ID. Si tratta di due repliche trasformate, con witness finiti e relazioni fornite dal codice, non di estrazione visiva autonoma, prova geometrica o generalizzazione a grafi arbitrari.

## Conseguenza pratica

Conviene fornire una vista del workspace limitata alla domanda, conservando integralmente le incidenze di tutte le alternative rilevanti. Questo riduce token e alcune accettazioni sbagliate. Il binding materiale va comunque verificato in codice su ID, uso completo del bordo e figura ospite. Le otto assegnazioni invalide accettate nello state ridotto restano errori Jev; un eventuale gate può respingerle ma non corregge retroattivamente questi conteggi. Non sono state aggiunte domande per una riparazione dei risultati.

## Richieste rifiutate e costo della prova

Il primo tentativo 39236236221 ha prodotto due risposte complete, poi si è fermato su un HTTP 400 della richiesta ridotta. Il diagnostico 39236455579 ha salvato soltanto flag fissi indicanti invalidità legata alle immagini, senza corpo del server e senza risposte native. Aggiungere un identico image_asset_manifest a entrambe le condizioni ha consentito il confronto completo, mantenendo espliciti i riferimenti a tutti gli asset dopo la rimozione degli snapshot. Il manifest contiene soltanto ID di immagini già presenti: lo state completo della misura finale è quello storico più questo elenco comune.

I due tentativi tecnici sono conservati separatamente. La misura finale ha 48 risposte; includendo le due del pilot iniziale sono 50 risposte native complessive e 27 richieste, di cui due HTTP 400. Non si confonde il successo del job diagnostico con una valutazione di binding riuscita.

La misura finale dichiara 153.060 token input e 1.866 output per lo state completo, 68.188 input e 1.848 output per quello ridotto: totale 221.248 input e 3.714 output. Il numero di domande è uguale alla prova precedente, ma l'uso di 24 richieste piccole ripete il workspace più volte rispetto alle precedenti quattro chiamate da dodici domande, che avevano consumato 59.040 token input. La riduzione del costo per chiamata non significa quindi un costo totale minore di quel benchmark. Il pilot iniziale aggiunge 10.250 input e 157 output dichiarati; usage delle due richieste rifiutate non disponibile.

Confidenza media dichiarata 0,535 sulle 48 risposte finali; affidabilità numerica e total_tokens non forniti, conservati come null o assenti. Le probabilità native arrotondate hanno deviazione massima dalla somma uno di 0,01 e non sono rinormalizzate. Non si interpreta la confidenza come garanzia di correttezza.

## Audit

Ricostruite tutte le 24 richieste e le dodici coppie di blocchi; verificate le 48 risposte typed, le immagini congelate, la proiezione di riferimenti, le 240 assegnazioni candidate, i binding del grafo e tutte le matrici. Gli input del modello non contengono gold, motivi di invalidità o risposte storiche. Live esclusivamente su Actions con secret TYPESAFE_API_KEY e header TypeSafe-Danger-Zone-Images: true. Nessun retry automatico, long context, nuova domanda Score o esposizione della chiave. Viewer offline, risultati sanitizzati, immagini e tentativi tecnici sono salvati in outputs e Library. Più immagini non dimostrano ragionamento sequenziale interno.
