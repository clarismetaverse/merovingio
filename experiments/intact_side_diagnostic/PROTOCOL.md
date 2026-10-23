# Lato intatto: controllo di formulazione e accesso alle premesse

Protocollo fissato prima di nuove chiamate. Fonte: esperimento multi_bridge_relevance, run 39940956209, solo obiettivo intact_anchor. Si riprendono i tre bridge individuali, le due presentazioni ruotate/riflesse, gli stessi ID, ordine dei candidati e byte PNG archiviati. Non si introducono classi o nuove geometrie. Tutti i candidati sono già verificati per entrambi i contratti locali storici dei Generic Spaces.

## Tre condizioni

1. **current**: descrizione attuale dell'obiettivo, identica all'archivio: “Prepare a later comparison using a subfigure that retains the entire designated reference side as one intact anchor. The two ends of that reference side are interchangeable; no endpoint and no size balance is preferred.”
2. **explicit**: almeno una delle DUE NUOVE regioni deve contenere sul PROPRIO bordo tutto il lato originale designato. La conservazione nel solo host o l'unione di pezzi appartenenti a regioni diverse non soddisfano la richiesta. Riferimenti ai Mental Spaces e lato designato invariati.
3. **coverage**: stesso testo explicit, con una tabella certificata di copertura di TUTTI i tre lati originali da parte di OGNUNA delle due regioni di OGNI candidato. Nessun verdetto complessivo sul candidato o indicazione del lato corretto nella tabella.

La domanda è identica in tutte le condizioni: `Does this candidate supply a subfigure that satisfies the active objective?` con riferimento al candidato e all'obiettivo. Una sola domanda **Noul** per candidato/versione: probabilità nativa di sì, nessuna scala di pertinenza, nessun Score o composito. Tre domande per richiesta, sei richieste, **18 giudizi**. Ordine delle sei richieste randomizzato con seed 2026102304. Ordine delle domande fissato per presentazione e uguale nelle tre condizioni. Nessun retry, follow-up o long context.

La policy generale è sostituita uniformemente nelle tre versioni per rimuovere vecchie istruzioni di scoring. Tutti gli altri fatti di workspace/state, immagini, Mental Spaces, Generic Spaces e region_vertex_cycles restano invariati. Il confronto current→explicit modifica solo active_objective.description. Il confronto explicit→coverage aggiunge solo certified_original_side_coverage. Il baseline current è una NUOVA valutazione binaria: il confronto con i precedenti Score non isola il tipo di domanda.

## Certificazione e riferimento esterno

Il codice calcola la proiezione delle boundary_uses collineari di ogni regione su ogni lato originale, interseca con [0,1] e unisce intervalli sovrapposti/adiacenti. Espone intervalli, frazione e complete/partial/none, con tolleranza geometrica 1e-7 pixel e di fusione 1e-7 in parametro. Due usi consecutivi nella STESSA regione possono coprire tutto il lato; pezzi in regioni DISTINTE non vengono aggregati. La certificazione non consulta l'obiettivo, la risposta o la funzione di utilità. È un controllo locale di questa geometria esplicita, non un certificatore generale del motore Merovingio.

Riferimento observer-only: due tagli (dai vertici alla base) conservano tutto il lato designato su una regione; il taglio dall'apice lo divide fra le due. Il riferimento precedente basato sui vertici viene ricontrollato usando la copertura del bordo. In ciascuna condizione: quattro positivi e due negativi. “Sempre sì” dà **4/6**: serve osservare anche i negativi.

## Analisi preregistrata

- Decisione fissa p>.5 sì, p<.5 no, p=.5 astensione, contata errata nell'accuratezza. Nessuna ricerca di soglie o fasce successive.
- Matrici TP/FN/FP/TN e astensioni separate per segno; accuratezza e probabilità native per ogni caso. Brier medio descrittivo: il campione non calibra le probabilità.
- Confronti appaiati current→explicit ed explicit→coverage: migliorati, peggiorati, entrambi corretti/errati. Nessun test di significatività su sei casi correlati.
- La correttezza di current è misurata rispetto all'interpretazione operativa dichiarata del lato sul bordo della sottofigura; un errore può quindi riflettere ambiguità, non necessariamente incapacità geometrica.

## Interpretazione e sicurezza operativa

Un recupero con explicit è compatibile con ambiguità di formulazione. Un recupero aggiuntivo con coverage è compatibile con difficoltà a recuperare le incidenze/ID dal contesto, non prova una causa interna. Il mancato recupero anche con coverage suggerisce verificare l'applicazione della richiesta alle premesse esplicite; non autorizza conclusioni generali su Jev. Sono tre costruzioni su un host e due presentazioni, non sei geometrie indipendenti. Nessuna distinzione fra limite visivo e testuale puro: tutte le condizioni mantengono le immagini.

Chiamate solo da GitHub Actions, modello jev-1.14.0, secret TYPESAFE_API_KEY, header TypeSafe-Danger-Zone-Images: true. Il runner e il transport bloccano esecuzioni live locali. Gli artifact contengono input ricostruibili, hash dei byte originali, risposte sanificate con Noul/usage e affidabilità/confidenza numerica se presenti; campi assenti restano null. Noul normalmente non ha confidenza separata. Errori HTTP/schema sono etichette fisse, senza corpi o eccezioni potenzialmente sensibili.

Le tabelle forniscono intenzionalmente premesse: non misuriamo estrazione autonoma da immagini, prova geometrica, pertinenza aperta o ragionamento temporale interno. Le immagini sono alternative prospective, non una sequenza di costruzione. SAME_FINAL_STATE != SAME_GENEALOGY resta il quadro storico; questo controllo riguarda l'interpretazione di una proprietà locale della trasformazione strutturale.

Documentazione Noul: https://docs.typesafe.ai/primitives/noul

## Ripresa tecnica, senza cambiare domande o input

Il run 39946481728 si è interrotto dopo la prima richiesta (coverage, presentazione 0) per un errore di formattazione del viewer sulle condizioni ancora vuote. I tre giudizi sono stati salvati integralmente in interrupted_run.json. Dopo la correzione del solo reporting, la ripresa verifica hash, input, metadati e risposte sanificate dell'artifact e riusa questa richiesta senza inviarla di nuovo. Esegue le cinque richieste mancanti nell'ordine originario. Ogni risposta conserva run e commit di effettiva esecuzione; il campione totale resta 18 giudizi, senza retry o selezione di risposte.
