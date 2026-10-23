# Dall’intento alle prospettive: pilot semantico, prima del binding

Protocollo e annotazioni congelati prima del live, su branch dedicato da `6854789f4bf92974b9411c6a41c8340c82be9ea2`. `main` e i precedenti esperimenti rimangono preservati.

## La decisione nuova

Il codice non ricava un’intenzione umana dai soli vincoli geometrici. JEV riceve sei richieste informali italiane riferite allo stesso workspace e un catalogo di tre prospettive. Propone quali prospettive esplorare, senza esaminare incidenze, scegliere ID geometrici, certificare un GS o soddisfare un predicato geometrico. È un test preliminare di instradamento semantico, non un altro test di validità chiamato “pertinenza”.

Le prospettive sono due contratti locali storici (`GS_HIST_DOUBLE_TRIANGLE`, `GS_HIST_MEDIAL_POLYROLE`) e la proposta di grammatica già presente `NEW_CONGRUENT_PAIR`. Quest’ultima **non** è un terzo GS storico. Titoli e descrizioni semantiche sono scritti dall’autore per il catalogo, non estratti automaticamente né considerati prove. Il corpus non rappresenta tutta Euclide.

Il workspace è il triangolo `left` già usato nei benchmark. Un catalogo finito di tre costruzioni prospettiche (`from_A`, `from_B`, `from_C`) è affidato esclusivamente al codice. I due contratti storici controllano tipo delle regioni, identità materiale, uso completo del carrier, adiacenza, contenimento e, per il secondo, copertura dell’host. Per la congruenza il codice confronta i tre lati ordinati dei due triangoli con tolleranza assoluta 1e-6 pixel: è un controllo numerico SSS sui fixture, non un theorem prover.

## Budget: una chiamata, sei Choice

Una domanda nativa `choice` per intento, tutte nella stessa richiesta. Ogni domanda offre le otto parti dell’insieme di tre prospettive (compreso l’insieme vuoto, “nessuna”) più “chiarire la richiesta”: nove opzioni. Un’opzione può contenere due o tre prospettive, senza vincitore interno. Questo evita di interpretare una distribuzione su opzioni singole come prova di rilevanza simultanea.

Seed 2026102308; alias dei frame, ordine degli intenti, ordine e alias delle opzioni randomizzati prima del live. Gli stessi frame mantengono gli stessi alias tra le domande; le opzioni hanno mapping esterno per domanda. `fixture.json` congela corpo completo, mapping e riferimenti esterni. Le istruzioni non contengono etichette della risposta corretta. Tutti gli intenti condividono uno state: non sono repliche indipendenti o conversazioni sequenziali.

1. Confrontare due pezzi triangolari adiacenti sul tratto comune: riferimento `{triangles}`.
2. Seguire lo stesso oggetto nei ruoli bordo/partizione: `{polyrole}`.
3. Richiedere entrambe le letture: `{triangles, polyrole}`.
4. Cercare parti sovrapponibili senza deformazioni: `{congruence}`, **anche quando il codice non trova binding nel catalogo dei tre tagli**.
5. Chiedere un numero per l’area: insieme vuoto, perché il catalogo non contiene un calcolatore numerico. Non significa che l’area non sia calcolabile.
6. Richiesta senza fuoco: due risposte accettabili, chiarire oppure mantenere aperte tutte le prospettive. Nessun gold unico imposto.

Queste sono **annotazioni proposte dall’autore**, fissate senza risposte JEV. Non sono valutazioni umane indipendenti, gold oggettivi di utilità né un test su parafrasi tenute da parte. Anche l’accettazione esatta dei set espliciti dipende dalla policy di catalogo adottata; il disaccordo merita lettura, non una diagnosi automatica d’incapacità.

## Separazione dei dati

Payload: descrizione minima del workspace e tipi di Mental Spaces, catalogo semantico con alias, sei testi, policy, domande e opzioni. **Non inviamo immagini**, coordinate, bridge, disponibilità delle prospettive, verdetti, riferimenti d’autore, risposte precedenti o certificati. L’assenza di immagini è intenzionale per isolare il nuovo ruolo; le tre illustrazioni del viewer sono solo per il lettore e il loro file non entra nel payload.

JEV interpreta la richiesta anche quando il frame desiderato non è attualmente istanziabile. Dopo la scelta, il codice esegue soltanto i controlli dei frame selezionati sui tre tagli; non corregge la risposta semantica e non sostituisce un frame non disponibile con uno diverso. Chiarimento e insieme vuoto eseguono zero controlli. L’inventario completo observer-only è calcolato offline per audit, fuori dall’input. La stessa mappa di dispatch viene usata per JEV e baseline.

## Confronti congelati e limiti

Due baseline senza chiamate: (a) conta esatta dell’intersezione di token normalizzati fra intento e titolo+descrizione di ogni frame, stopword nel codice, selezione di tutti i massimi a punteggio positivo, vuoto se nessuno; (b) esplora sempre tutti e tre. Nessun adattamento del lessico o della soglia ai risultati. Il confronto lessicale è debole e trasparente, non uno stato dell’arte del retrieval. “Esplora tutto” privilegia richiamo senza interpretare l’intento.

Riportiamo tutti i set scelti, probabilità e confidenza nativa, accettabilità secondo le annotazioni, matrice per sistema, risultati di dispatch, frame selezionati senza binding, numero di binding e unità di lavoro (un controllo frame/taglio). Queste unità sono **contabilità deterministica**, non latenza o risparmio economico misurati. I due GS storici possono produrre gli stessi bridge con letture diverse: non rivendichiamo un vantaggio nella selezione geometrica dei candidati. Un maggior numero di binding non equivale a maggior utilità.

Non applichiamo soglie di confidenza, compositi, correzioni automatiche, rilanci o ottimizzazione successiva. “Nessun binding trovato” significa soltanto assenza nei tre tagli controllati, non impossibilità matematica. Nessuna scoperta libera di GS, prova, comprensione visiva, ragionamento sequenziale interno o utilità di prodotto dimostrata. Prima di una conclusione di valore incrementale servono annotatori indipendenti, intenti nuovi e una baseline più forte.

## Esecuzione e conservazione

Solo GitHub Actions, modello `jev-1.14.0`, secret `TYPESAFE_API_KEY`, header `TypeSafe-Danger-Zone-Images: true` anche per questa richiesta testuale. Guardie sia nell’entrypoint sia nel trasporto. Una sola richiesta, timeout 180 s, nessun retry. Risposte conservate tramite allowlist: opzioni ammesse, probabilità numeriche, confidenza, affidabilità se restituita e usage; nessun testo libero del server, header di autenticazione o corpo di errore. Mancanze non diventano zeri. Qualunque fallimento resta esplicito e non viene presentato come risposta sperimentale.

Test offline per contratto di input, budget, mapping, set multipli, disponibilità separata dalla semantica, controlli geometrici e sanificazione. Audit ricostruisce input e risultati, verifica fixture e stato finale. Pipeline include i test storici e la build del viewer esistente. Artifact scaricato con viewer offline, protocollo, JSON e immagini per il lettore; nessun risultato inventato prima del completamento.

Riferimenti API: [Choice](https://docs.typesafe.ai/primitives/choice), [intent routing](https://docs.typesafe.ai/patterns/intent-routing).
