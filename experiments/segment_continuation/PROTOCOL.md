# Continuazione del segmento: otto domande, prima del live

Branch dedicato da `90083c9c27e8ecd48bd81668c46b25bb38ba46fb`; main e tutta la catena v0.9/v1.0 e benchmark precedenti preservati. Protocollo, renderer, opzioni e riferimenti congelati prima delle risposte.

## Costrutto e geometria

Due storie di tre osservazioni di un unico segmento. Nella prima A si allontana da B, che resta fermo; nella seconda B si allontana da A, che resta fermo. Le lunghezze a ogni istante coincidono tra storie (100, 125, 150 pixel) e il segmento finale è **lo stesso PNG**, con gli stessi ID e colori. Una riflessione dell’asse locale x, seguita da una rotazione 3-4-5 (cos=.8, sin=.6), è applicata uniformemente. Un’unica trasformazione live, non una valutazione fattoriale di robustezza.

Regola fornita: continuare la stessa modifica di un passo uguale al precedente, mantenendo fermo l’estremo che era fermo. La regola rende il passo unico con la cronologia completa. Senza questa assunzione, una sequenza non determina una sola intenzione futura. Il modello non deve inventare una costruzione libera o dimostrare un teorema.

Cinque passi successivi visivi comuni: estendere A, estendere B, accorciare A, accorciare B, mantenere il segmento. Una sesta opzione testuale indica informazioni insufficienti. È distinta dal mantenere invariata la figura. Tutti i segmenti proposti sono non degeneri e sulla stessa retta; soltanto due sono prolungamenti. Il codice verifica coordinate, collinearità, identità dell’estremo fermo, lunghezze e passo di 25 pixel. La continuazione viene controllata prima della chiamata ed è observer-only.

Le immagini hanno canvas 384×384, tratto scuro di 4 pixel, punti di raggio 6, lettere A/B. Blu e ambra identificano gli estremi e sono invarianti tra storie e alternative; non codificano la risposta. Nessuna freccia, evidenziazione del vincitore o gold nelle immagini. La palette e le identità sono dichiarate uniformemente. Alcuni disegni delle alternative coincidono con osservazioni passate: non sono immagini nuove soltanto perché usate come opzioni. Il manifest deduplica per scena e congela hash e riferimenti opachi.

## Due storie × quattro condizioni = otto Choice

Otto contesti indipendenti, una domanda nativa `choice` per richiesta. Questo impedisce che l’altra storia o un’altra modalità nello stesso state fornisca l’informazione mancante. Non ci sono conversazioni con memoria o chiamate dipendenti fra frame. Ordine delle otto richieste e ordine/alias delle sei opzioni fissati con seed 2026102309. Opzioni, descrizioni e alias sono identici in ogni cella, per isolare l’evidenza. I riferimenti agli asset sono UUID opachi; nessun nome di storia/azione entra nel payload.

| Condizione | Osservazioni | Alternative |
|---|---|---|
| final_only | Solo immagine finale comune | Cinque immagini + insufficienza |
| images | Tre immagini in ordine cronologico | Identiche |
| text_history | Tre record di coordinate A/B, con convenzione pixel | Identiche immagini |
| combined | Stesse tre immagini e stessi record testuali | Identiche |

La condizione testuale **non è priva di immagini**: il modello deve collegare le coordinate alle alternative visive. Non contiene frasi “A si muove” o un’etichetta del passo corretto: solo coordinate osservate, ordine e convenzione. Combined aggiunge soltanto quelle coordinate a images. Le immagini non possono essere accreditate per un eventuale risultato già ottenibile con le coordinate.

I due controlli final-only hanno corpi di richiesta **esattamente identici**, pur appartenendo a storie esterne diverse: sono due esposizioni pianificate, non retry. Senza cronologia non esiste un next-step gold unico; `next_step_accuracy` e `reference_next_action` restano null. Riportiamo astensioni e proposte non supportate come comportamento di controllo, senza chiamare “successo” un 50% di scelte fra estremi.

## Baseline di tracciamento indipendente

Il tracker raster legge soltanto i PNG realmente inviati: trova il baricentro dei pixel dei due colori, calcola gli spostamenti consecutivi, richiede un solo estremo in moto a velocità costante e predice il passo successivo. Confronta poi la previsione con i centri degli estremi estratti dai PNG delle alternative. Non legge nome di storia, coordinate del renderer, riferimento o etichetta corretta. La mappa opaca delle opzioni viene decodificata dopo la selezione, come per JEV. Nessuna osservazione precedente implica astensione.

È una baseline specializzata per palette pulita, marker separabili, identità stabili e trasformazione a passo costante; non è un sistema generale di visione. Tolleranza pixel 1; movimenti reali 25 pixel; posizioni intere grazie alla rotazione scelta. Un tracker testuale usa gli stessi calcoli sulle coordinate fornite, mantenendo il confronto con le opzioni raster. Nei casi combined riportiamo entrambi; nei casi testuali il confronto principale è il tracker testuale, negli altri quello raster. Disponibilità della baseline e accuracy geometrica sono separate dall’output del modello.

## Analisi fissata

Per ogni condizione: tutte le opzioni scelte e distribuzioni, confidenza e affidabilità numerica se restituita, matrici, successi identificabili / 2, astensioni, failure e baseline. Nel controllo finale nessuna accuracy di continuazione, soltanto conteggi di insufficienza/proposte non giustificate. Descrivere se entrambi gli estremi/storie sono corretti, non soltanto l’aggregato. Confronti appaiati images↔testo, images↔combined e testo↔combined sulle stesse due storie. Nessun composito o soglia adattata dopo il live.

Otto risposte non stimano significatività o generalizzazione. Il budget non include ordine inverso, shuffle, fotogramma intermedio isolato o un ulteriore controllo completamente testuale. Due osservazioni distinte sono sufficienti per il tracker: un vantaggio rispetto al finale non dimostra necessità di tre frame o elaborazione sequenziale interna. Proporre un’opzione già disegnata non equivale a generare un segmento o coordinate nuove. Il successo su un fixture sintetico non dimostra utilità rispetto al codice se il workspace possiede già il log delle operazioni.

## Esecuzione e integrità

Solo Actions, modello `jev-1.14.0`, secret `TYPESAFE_API_KEY`, header `TypeSafe-Danger-Zone-Images: true`. Guardie nel runner e nel trasporto riusato dal benchmark semantico. Timeout 180 s, nessun retry, nessuna correzione del prompt o chiamata aggiuntiva in base agli esiti. Reiezioni 400/401/403 interrompono e salvano il parziale; altre failure sono conservate e non trasformate in risposte. Sanificazione tipizzata/numerica già verificata, nessun corpo libero o chiave salvata.

Immagini e manifest congelati prima del live. Audit ricostruisce i corpi esatti, controlla PNG, osservazioni e alternative, riesegue entrambi i tracker e ricalcola l’analisi. Test offline geometrici, di non-leakage e controllo non identificabile, suite storiche e build in pipeline. JSON live originale preservato; pacchetto finale con viewer offline, protocollo, risposte e metadati CI scaricato e archiviato in Library.

API: [immagini anche nei criteri Choice](https://docs.typesafe.ai/images), [Choice nativo](https://docs.typesafe.ai/primitives/choice).
