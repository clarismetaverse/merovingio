# Coppia errata del rettangolo: orientazione e ID separati

Protocollo fissato prima delle nuove chiamate. Sorgente: run 39994076040, commit 89cea8410acef74f276f5d94fb9bf65f2b083f8a. Si mantengono i due bridge della coppia C914/C850: B_to_near_C è positivo, C_to_near_B è negativo. Nel run storico, con quattro candidati, P(sì) era rispettivamente .41/.51. Quelle risposte non entrano nel nuovo input.

## Disegno e budget

Quattro condizioni incrociano due fattori, con **due Noul per richiesta, otto giudizi complessivi**:

| Cella | Orientazione | ID |
|---|---|---|
| original | originale | originali |
| orientation_only | sola rotazione | originali |
| ids_only | originale | nuovi |
| orientation_and_ids | stessa rotazione | stessi nuovi |

Una sola domanda binaria per bridge, con testo e policy identici al controllo explicit. Nessuna tabella di copertura, Score, composito, riparazione o retry. Ordine delle quattro richieste randomizzato prima del live con seed 2026102306. Ordine dei due candidati e delle domande Q001/Q003 mantenuto in tutte le celle: variare l'ordine introdurrebbe un ulteriore fattore.

## Contesto comune e baseline fresco

Si ricostruisce prima il corpo della richiesta storica completa verificandone l'hash e i byte PNG. Poi si rimuovono, identicamente in tutte le quattro celle, gli altri due candidati, le loro immagini e domande. Restano tutti i Mental/Generic Spaces, le descrizioni astratte, i contratti, i fatti materiali/metrici dei due bridge, il lato designato e la richiesta esplicita originali.

Il baseline original è quindi una NUOVA richiesta su una coppia isolata. Riusa i tre PNG originali (host e due bridge) e tutti i fatti residui esatti, ma non ripete il contesto precedente di quattro candidati. Se l'errore non si riproduce qui, non si può attribuire il recupero alla rotazione o agli ID. La riduzione del contesto è comune alle quattro condizioni e il confronto storico non la separa dalla variabilità fra chiamate.

## Orientazione: una rotazione rigida, riflessione fissa

Il rettangolo storico era ruotato di 51° e riflesso. L'intervento applica −51° intorno al centro fisso (160,160), conservando riflessione, scala, centro e identità degli oggetti. Il lato designato diventa orizzontale. Nessun nuovo bridge, allungamento o spostamento indipendente degli endpoint. Distanze, incidenze, cicli, materiali, regioni e riferimento restano invariati.

Nel payload di orientation_only lo state e le domande restano esattamente identici a original: cambiano solo i byte dei PNG. Non si ricalcolano o sostituiscono i fatti metrici forniti al modello. Il nuovo rendering usa stesso canvas 320×320, stile, font e dimensione dei caratteri; rotazione e rasterizzazione possono modificare l'aspetto delle linee e la posizione delle etichette. Non è un isolamento di un algoritmo visivo interno.

## ID: una sola biiezione coerente, nessuna permutazione dei ruoli

La rinomina sostituisce con alias neutri disgiunti i punti, i candidati, i carrier materiali, le regioni, gli identificatori dei Mental e Generic Spaces e i riferimenti alle immagini dei candidati. È la STESSA biiezione in ids_only e orientation_and_ids, applicata sia alle chiavi sia ai valori di riferimento e alle lettere nelle immagini. Le posizioni dei candidati e il binding dei ruoli agli oggetti non cambiano.

Nomi semantici di ruoli/tipi/predicati, descrizioni e contratti rimangono letteralmente invariati. L'ID di contesto host, initial e i question IDs restano costanti. Applicare la biiezione inversa ricostruisce esattamente lo state e le domande del baseline per tutte le quattro celle. Nei PNG a orientazione fissa, i pixel modificati dalla rinomina sono confinati ai glifi delle etichette. Il test varia insieme nomi visibili e riferimenti strutturati; non distingue un limite dei nomi testuali da uno della lettura delle lettere nei pixel.

## Verifiche e analisi preregistrata

I due bridge vengono ricontrollati dal codice per entrambi i contratti materiali storici in entrambe le orientazioni: due triangoli adiacenti, stesso carrier usato interamente da entrambi, interni disgiunti e partizione completa dell'host. Il riferimento sul lato intatto viene ricomputato esternamente su ogni geometria. Non si invia né si salva una nuova tabella di copertura nel payload; il codice usa internamente la verifica precedente del bordo per il riferimento.

Soglia fissa p>.5 sì, p<.5 no, p=.5 astensione contata errata. Si riportano probabilità grezze, matrici e Brier descrittivo per cella. Margine = P(sì)_positivo − P(sì)_negativo. Contrasti: differenza di ogni probabilità e del margine cambiando un fattore alla volta a ciascun livello dell'altro; interazione descrittiva dei margini m11−m10−m01+m00. Queste differenze tra risposte native non sono uno scoring composito e non cambiano la soglia di successo.

Si registra se il baseline fresco riproduce entrambi i giudizi errati non astenuti dello storico. Una coppia preselezionata perché errata, una sola nuova orientazione, una sola rinomina e una risposta per cella non permettono test di significatività o inferenze generali. Il contesto comune pruned e la variabilità delle chiamate limitano le interpretazioni storiche; gli interventi non spiegano il processo interno di Jev.

## Riproducibilità e trasporto

I PNG e il manifest di geometrie e biiezione sono congelati nel repo prima del live. Il baseline conserva i byte storici esatti. I test verificano anche che il renderer riproduca i PNG originali prima delle trasformazioni, la conservazione delle distanze e della chiralità, l'assenza di leakage e l'invertibilità della rinomina.

Chiamate esclusivamente via GitHub Actions, modello jev-1.14.0, secret TYPESAFE_API_KEY e header TypeSafe-Danger-Zone-Images: true. Guardie nel runner e nel trasporto; nessuna chiamata live locale. Risposte native sanificate con Noul/usage, confidenza e affidabilità numerica se presenti, altrimenti null. Nessuna chiave o corpo di errore negli artifact. Nessuna prova geometrica, scoperta libera di GS o ragionamento sequenziale interno viene dimostrato.
