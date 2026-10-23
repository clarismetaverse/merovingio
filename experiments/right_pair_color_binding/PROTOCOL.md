# Colori su segmenti e punti: identità visiva della stessa coppia

Protocollo fissato prima del live. Stessi bridge C914 positivo e C850 negativo del rettangolo, stessa orientazione originale di 51° e riflessione, stessi ID, ordine, richiesta esplicita, contratti e fatti strutturati. Il precedente baseline isolato del run 39996906771 restituiva .67/.51; quei valori restano fuori dal nuovo input.

## Tre condizioni, sei giudizi

1. **monochrome**: nuova chiamata con il corpo esatto del baseline isolato precedente, verificato per hash. PNG originali, nessuna variazione del contesto.
2. **color**: stesso state e stesse due domande; cambiano soltanto i valori RGB dei PNG.
3. **color_legend**: stessi identici byte colorati della seconda condizione, più una legenda testuale di associazione colori→ID. Nessuna nuova incidenza o proprietà geometrica.

Una Noul per candidato/versione, due per richiesta, tre richieste: **sei giudizi nuovi**. Il replay del baseline è intenzionale per confrontare i colori con una misurazione contemporanea, non un retry. Nessuna ripetizione automatica, domanda aggiuntiva, Score, composito o tabella di copertura. Ordine delle tre richieste randomizzato con seed 2026102307; ordine dei candidati e delle domande Q001/Q003 fisso per non aggiungere un fattore.

## Colore senza risposta suggerita

I tre lati originali hanno colori distinti e stabili per identità: AB ambra, BC blu, CA verde acqua. I tre vertici originali hanno colori stabili per punto. Entrambi i nuovi carrier sono viola; entrambi i nuovi punti di contatto sono magenta. La palette dipende dall'oggetto o dal tipo di elemento disegnato, non dal riferimento positivo/negativo o dall'obiettivo. Non si segnano risposte giuste/sbagliate con colori, né si riempiono regioni.

Le lettere degli ID restano scure. Canvas 320×320, coordinate, spessore delle linee (3 px), raggio dei punti (3 px), font/dimensione/posizione delle etichette e interni bianchi sono identici. I test confrontano tutti i pixel e verificano che la maschera non-bianca sia esattamente invariata: nessun segmento, punto, vuoto o glifo viene aggiunto o spostato. Il renderer monocromatico riproduce i pixel storici prima di applicare i colori.

La legenda elenca uniformemente tutti e tre i lati originali tramite Mental Space/endpoints già esistenti, tutti e cinque i punti visibili e i due nuovi carrier materiali. Colori condivisi possono indicare il tipo di disegno; non fondono materialmente due oggetti distinti di candidati alternativi. Non vengono forniti cicli aggiuntivi, appartenenze a lati, frazioni/intervalli di copertura, verdetti complessivi, ranking o etichette di utilità.

## Analisi preregistrata

Soglia invariata: p>.5 sì, p<.5 no; p=.5 astensione contata errata. Probabilità native, TP/FN/TN/FP e astensioni per versione, Brier descrittivo e margine P(sì)_positivo−P(sì)_negativo. Contrasti previsti: differenze di ogni probabilità e del margine fra mono→color e color→color_legend. Il margine non è un composito di dimensioni, non modifica la soglia e non sostituisce il riconoscimento corretto del negativo.

Il confronto mono→color testa un cambiamento soltanto visivo. Color→color_legend testa l'accessibilità dell'associazione esplicita fra colori e ID, usando immagini pixel-identiche. Se il nuovo replay monocromatico cambia rispetto a .67/.51, non attribuiamo tale variazione ai colori. Una coppia preselezionata per errore, una sola palette e una chiamata per condizione non stimano variabilità, significatività o generalizzazione. Non cambiamo palette o soglia dopo i risultati.

## Codice e riproducibilità

Entrambi i bridge sono ricontrollati per i due contratti locali storici dei Generic Spaces e per il riferimento sul lato intatto. Sono tutti formalmente ammissibili; il negativo manca soltanto lo specifico requisito dell'obiettivo. Nessun riferimento o tabella di copertura entra nel payload.

Sei PNG unici congelati prima del live (tre monocromatici e tre colorati); color e color_legend condividono gli stessi file. Il manifest registra palette, legenda e hash. L'audit ricostruisce tutti i corpi effettivi, verifica il replay esatto del baseline, le invarianze fra condizioni e le risposte sanificate.

Chiamate esclusivamente da GitHub Actions, modello jev-1.14.0, repository secret TYPESAFE_API_KEY e header TypeSafe-Danger-Zone-Images: true, con blocco live locale anche nel trasporto. Nessun long context, retry automatico o corpo d'errore libero. Noul e usage preservati; confidenza/affidabilità numerica solo se restituite, altrimenti null. Immagini e state rimangono insieme: nessuna prova geometrica, estrazione autonoma dai pixel, scoperta libera di GS o ragionamento sequenziale interno è implicato.
