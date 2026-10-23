# Intento → prospettive: primo risultato verificato

La [pipeline live 40003906109](https://github.com/clarismetaverse/merovingio/actions/runs/40003906109) è completata con successo sul commit `3406ed826fa3bf9cd0a28acb437d02dee8d5d13c`. **Una sola chiamata JEV 1.14, sei Choice native, zero retry e zero failure.** Protocollo, annotazioni e fixture sono presenti in quel commit, prima della chiamata. La risposta sanificata esatta è conservata in `live_results.json`.

## Cosa è stato chiesto

Interpretare sei intenzioni informali riferite allo stesso workspace e scegliere un insieme di prospettive da esplorare. JEV non ha ricevuto immagini, coordinate, bridge, binding, disponibilità dei frame o annotazioni di riferimento. Le tre immagini del viewer sono illustrazioni per il lettore. Due prospettive rimandano ai contratti locali di GS storici; la congruenza è una proposta di grammatica già presente, non un terzo GS storico.

## Tutte le risposte

| Intento | Scelta JEV | P(opzione scelta) | Confidenza nativa | Esito secondo le annotazioni proposte |
|---|---|---:|---:|---|
| Confrontare parti triangolari sul tratto comune | triangles | .99 | .99 | Accettabile |
| Seguire lo stesso oggetto nei ruoli bordo/partizione | polyrole | 1.00 | 1.00 | Accettabile |
| Usare entrambe le letture | {triangles, polyrole} | 1.00 | 1.00 | Accettabile |
| Cercare parti sovrapponibili senza deformazioni | congruence | 1.00 | 1.00 | Accettabile semanticamente; nessun binding nei tre tagli |
| Ottenere un numero per l’area | none | .99 | .99 | Fuori dal catalogo, correttamente instradato altrove |
| Capire la figura senza specificare un confronto | clarify | .57 | .52 | Una delle due azioni accettabili; anche mantenere aperti tutti i frame era ammesso |

Confidenza e probabilità sono uscite native non calibrate; non provano correttezza né una probabilità oggettiva d’utilità. La domanda ambigua non ha un gold unico. Le distribuzioni complete sono conservate, non sostituite dalla sola opzione massima. Affidabilità separata non restituita: `null`.

## Confronti fissati prima del live

| Sistema | Azioni accettabili / 6 | Controlli frame/taglio | Binding restituiti |
|---|---:|---:|---:|
| JEV | 6/6 | 15 | 12 |
| Intersezione esatta di token, massimi pari ammessi | 4/6 | 18 | 15 |
| Esplorare sempre tutti i frame | 1/6 | 54 | 36 |

La baseline lessicale manca la richiesta doppia (seleziona solo polyrole) e quella vaga (seleziona due frame invece di chiarire o lasciare tutte le prospettive aperte). JEV differisce proprio in questi due casi. La baseline esplora-tutto favorisce il richiamo senza interpretare l’intento: il suo basso accordo con i set minimi non è una misura generale della sua inutilità.

Le 15/18/54 sono **unità di lavoro convenzionali**, non tempi o costi misurati. L’inventario completo è comunque calcolato offline per audit. I due contratti storici sono validi per tutti e tre i tagli e restituiscono gli stessi candidati sotto letture diverse: non abbiamo mostrato una migliore scelta geometrica del bridge.

Il caso più informativo è la congruenza: JEV riconosce l’interesse semantico, poi il codice controlla i tre lati ordinati dei triangoli e restituisce zero binding. Il sistema non scambia l’intenzione per un fatto geometrico, non ripiega su un altro frame e non dichiara impossibile una costruzione fuori dal catalogo finito. Due GS validi non diventano automaticamente pertinenti a qualunque richiesta.

## Esecuzione e audit

Chiamata soltanto in Actions con secret `TYPESAFE_API_KEY` e header `TypeSafe-Danger-Zone-Images: true`. Usage restituito: **3880 input token, 663 output token**, totale non restituito (`null`). Durata del solo trasporto registrata: circa 0.147 s, una misura isolata non comparabile a un benchmark di latenza. Sei confidenze native presenti; nessuna affidabilità numerica separata.

Fixture canonica SHA256: `6bdc966db6770fa4ec0e1c3147b368ec6ee3e5b3d3d76af16f9cbe40830133c3`. Audit ricostruisce la richiesta completa, verifica tutte le sei risposte native, ricalcola dispatch e matrici dei tre sistemi con tolleranza 1e-12 per numeri rigenerati. JSON originario conservato senza riscrittura. Test storici e nuovi, build viewer e audit hanno superato la pipeline; i dettagli dell’esecuzione sono nei metadati CI del pacchetto finale. Nessun risultato delle prove precedenti viene modificato.

## Interpretazione

È un segnale favorevole per un ruolo più delimitato: **intenzione informale → prospettive; codice → binding, vincoli e disponibilità**. Non è una dimostrazione che “abbiamo trovato il ruolo definitivo”. Sei richieste sintetiche sono scritte dallo stesso autore che descrive catalogo e riferimenti; non ci sono annotatori indipendenti, parafrasi tenute da parte o retrieval forte. Il vantaggio è due decisioni rispetto a una baseline volutamente semplice, non generalizzazione o utilità di prodotto già stabilita.

Prima di ampliare il catalogo conviene fissare intenti nuovi e accettabilità con persone indipendenti, confrontare una baseline più forte e misurare un beneficio a valle. Questa prova testuale non dice nulla di nuovo su immagini sequenziali, comprensione visiva, scoperta autonoma di GS o ragionamento sequenziale interno.
