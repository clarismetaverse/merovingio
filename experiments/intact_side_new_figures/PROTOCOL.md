# Richiesta esplicita su figure nuove, senza tabella di copertura

Protocollo fissato prima di chiamare Jev. Riprendiamo esattamente il testo explicit del controllo intact_side_diagnostic (run 39946781738), la policy generale e la domanda Noul per candidato. Il testo resta letteralmente uguale; cambiano figure, bridge e ID. Nessuna scala Score o composito.

## Campione e budget

Tre host triangolari nuovi, scaleni: acutangolo, rettangolo e ottusangolo. Non sono simili tra loro o al precedente isoscele. Una presentazione per host, con rotazioni 13°, 51°, −23° e riflessione del rettangolo. Non incrociamo orientazione e forma per contenere il budget: tre geometrie, non dodici campioni indipendenti.

Per ogni host, quattro bridge validi organizzati dall'osservatore in due coppie vicine, due positivi e due negativi. Una sola domanda nativa Noul per candidato, quattro domande per richiesta, tre richieste: **12 giudizi totali**, sei positivi e sei negativi. “Sempre sì” e “sempre no” fanno 6/12. Nessun nuovo controllo sul vecchio host, retry, domanda speculativa o riparazione. L'ordine delle richieste e delle domande, le etichette di punti/GS e gli ID/ordine dei candidati sono fissati con seed 2026102305 prima delle chiamate. Il modello non riceve i nomi delle famiglie, dei metodi o delle coppie.

## Costruzione dei controesempi vicini

Il lato originale designato è AB nel generatore; il modello vede etichette randomizzate. Per il primo positivo, si taglia da A a un punto E su BC vicino a C; per il suo negativo, si taglia da C a un punto D su AB vicino ad A. I due segmenti sono entrambi vicini al bordo originale AC, ma solo il primo lascia AB intero sul bordo di una nuova regione. La seconda coppia ripete lo schema vicino a BC, partendo da B e poi spostando il contatto dentro AB vicino a B.

La frazione epsilon è .12 nell'acutangolo, .10 nel rettangolo e .14 nell'ottusangolo. Lo spostamento massimo fra endpoint abbinati dei due bridge non supera epsilon volte il lato più lungo del rispettivo host. Questa vicinanza è geometrica esplicita, non una soglia inventata sulle risposte del modello. Tutti i tagli sono distinti, interni, con regioni non degeneri e leggibili; nessun caso coincide con il bordo originale.

Il codice certifica entrambi i contratti locali storici per ogni candidato: due regioni triangolari adiacenti usano COMPLETAMENTE lo stesso carrier materiale; gli interni sono disgiunti e l'unione copre l'host. I negativi soddisfano tutti questi requisiti: sono controesempi alla conservazione del lato, non bridge formalmente invalidi. Si mantengono region_vertex_cycles, relazioni materiali, metriche, Mental Spaces e Generic Spaces già previsti dal formato precedente.

## Richiesta invariata e riferimento esterno

La richiesta impone che almeno una delle DUE NUOVE regioni abbia sul PROPRIO bordo tutto il lato originale designato. La conservazione nel solo host o la ricomposizione di pezzi appartenenti a regioni distinte non basta. Gli endpoint sono intercambiabili e il bilanciamento delle aree non è preferito.

La domanda resta: `Does this candidate supply a subfigure that satisfies the active objective?` con candidate_ref e objective_ref. Nessuna tabella certified_original_side_coverage, frazione di copertura, complete/partial/none per lato, etichetta di riferimento o verdetto sul candidato viene inviato a Jev. Le metriche e i binding materiali sono fatti forniti intenzionalmente; non contengono un verdetto complessivo sulla richiesta.

Il riferimento observer-only viene calcolato dai boundary_uses: proiezione dei segmenti collineari su AB e unione degli intervalli per ciascuna regione separatamente, usando il controllo precedente. Si ricontrolla indipendentemente la presenza dei due endpoint originali sul ciclo della stessa regione per queste fixture triangolari. Il riferimento non dipende dalle risposte. Le tabelle di copertura presenti nell'artifact sono esplicitamente observer_only_coverage e sono escluse dal payload.

## Analisi preregistrata

Soglia invariata: p>.5 sì, p<.5 no, p=.5 astensione contata errata. Matrici TP/FN/TN/FP e astensioni separate, accuratezza e Brier descrittivo complessivi e per figura, tutte le probabilità native. Sei coppie vicine: numero di coppie con entrambi i giudizi corretti e numero con p_positivo>p_negativo, con margini grezzi; l'ordine delle probabilità è diagnostico e non sostituisce la correttezza alla soglia fissata. Nessuna ottimizzazione di soglie, aggregazione o criterio di vincitore unico.

L'obiettivo è verificare se la formulazione esplicita si trasferisce a nuove geometrie e controesempi, non dimostrare pertinenza matematica generale o scoperta autonoma di Generic Spaces. Immagini e state strutturato restano insieme, quindi non isoliamo il contributo dei pixel. Il precedente 6/6 explicit è confronto storico descrittivo, non un controllo contemporaneo per stimare causalmente l'effetto della nuova forma.

## Riproducibilità e chiamate

I PNG e il manifest delle geometrie/ID sono congelati nel repository prima del live. Il runner verifica hash e coordinate e copia gli stessi byte su ogni piattaforma. Immagini monocrome con soli ID neutri, nessuna etichetta di risposta o metadato testuale. Build, test geometrici, pairing, non-leakage e ricostruzione delle richieste sono offline.

Chiamate solo via GitHub Actions, modello jev-1.14.0, secret TYPESAFE_API_KEY e header TypeSafe-Danger-Zone-Images: true; blocco live anche nel runner locale. Trasporto e sanificazione riutilizzano il controllo precedente. Le risposte conservano Noul e usage; affidabilità/confidenza numerica sono null se assenti. Nessuna chiave, eccezione libera o corpo di errore negli artifact. Nessuna prova geometrica, estrazione visiva autonoma o ragionamento sequenziale interno è implicata da questo esperimento.
