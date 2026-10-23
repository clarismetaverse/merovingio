# Coppia del rettangolo: orientazione e ID non eliminano il falso positivo

**Tutte le quattro condizioni fanno 1/2 alla soglia preregistrata .5.** Il positivo riceve sempre più di .5, ma anche il negativo resta fra .51 e .59. Né la sola rotazione, né la sola rinomina, né la loro combinazione risolvono il falso positivo di questa coppia.

Il [run live 39996906771](https://github.com/clarismetaverse/merovingio/actions/runs/39996906771) è completato con successo, commit `d53a94003d5098d8f62c44fceee7a2bac03a5fef`: **quattro richieste di due Noul, otto giudizi totali, nessun retry**, senza tabella di copertura, Score o composito. Bridge, richiesta esplicita, policy, contratti e ordine dei candidati sono invariati. I due bridge passano entrambi i contratti materiali storici in tutte le versioni.

| Condizione | P(sì), positivo | P(sì), negativo | Margine positivo − negativo | Corretti | Brier medio |
|---|---:|---:|---:|---:|---:|
| Coppia isolata, originale | .67 | .51 | +.16 | 1/2 | .18450 |
| Sola rotazione | .74 | .59 | +.15 | 1/2 | .20785 |
| Soli ID nuovi | .57 | .55 | +.02 | 1/2 | .24370 |
| Rotazione + ID nuovi | .76 | .51 | +.25 | 1/2 | .15885 |

In ogni cella: TP=1, FP=1, TN=0, FN=0, nessuna astensione. Totale **4/8**, uguale al baseline sempre sì su questo campione bilanciato. Le probabilità sono giudizi nativi di sì, non misure del grado di soddisfacimento della proprietà. Vicinanza a .5 indica una risposta poco separata, non una certezza del modello.

## Prima osservazione: i due errori storici non si riproducono insieme

Nel precedente run 39994076040, con quattro candidati, la coppia C914/C850 aveva rispettivamente .41/.51: falso negativo e falso positivo, ordine invertito. Il nuovo baseline, ancora con orientazione e ID originali ma **solo due candidati**, restituisce .67/.51: il positivo è già recuperato senza interventi su orientazione o ID. Il falso positivo resta.

Non si può quindi attribuire il recupero del positivo alla rotazione o alla rinomina. La rimozione comune degli altri due candidati e delle relative immagini/domande cambia il contesto rispetto allo storico; una singola nuova chiamata non separa questo effetto dalla variabilità delle risposte. Il baseline è fresco e conserva i byte originali delle tre immagini residue e tutti i fatti/domande residui esatti; non è una replica del vecchio contesto completo.

## Confronti con un solo fattore variato

| Contrasto preregistrato | Delta P(sì), positivo | Delta P(sì), negativo | Delta margine |
|---|---:|---:|---:|
| Rotazione, con ID originali | +.07 | +.08 | −.01 |
| ID nuovi, con orientazione originale | −.10 | +.04 | −.14 |
| Rotazione, con ID nuovi | +.19 | −.04 | +.23 |
| ID nuovi, con orientazione ruotata | +.02 | −.08 | +.10 |

Interazione descrittiva dei margini: +.24. È una differenza fra risposte native delle quattro celle, non uno scoring composito o un test statistico. Con una sola chiamata per cella non stimiamo rumore, significatività o una causa interna.

La sola rotazione con gli ID originali alza quasi allo stesso modo entrambe le probabilità e lascia il margine quasi identico. I soli ID nuovi portano la coppia vicino al pari (.57/.55). La combinazione ha il margine maggiore (+.25), ma non corregge il negativo a .51. Il positivo supera il negativo in tutte le quattro celle: questo ordinamento relativo è descrittivo e **non** viene contato come un riconoscimento corretto del negativo o come una validazione di ranking generale.

## Che cosa è stato tenuto fisso

- Coppia originale: C914 = B_to_near_C positivo; C850 = C_to_near_B negativo. La biiezione dei candidati li rinomina rispettivamente C113/C675, senza scambiare i ruoli o le posizioni.
- Orientazione: si annulla soltanto la rotazione di 51° intorno a (160,160), mantenendo la riflessione originaria, scala e centro. Nessun cambiamento di lunghezze, incidenze o regioni. Nei payload a ID fissi cambiano solo i PNG; state, certificati, metriche e domande restano esatti.
- ID: stessa biiezione in entrambe le orientazioni, applicata a punti/lettere, candidati, carrier, regioni, Mental/Generic Spaces e riferimenti delle immagini. Ruoli, tipi, predicati e descrizioni non cambiano; host, initial e question IDs restano costanti. La biiezione inversa ricostruisce esattamente state e domande del baseline in tutte le celle.
- La rinomina modifica insieme le lettere nei pixel e i riferimenti strutturati. Non isola il confronto di ID puramente testuali. Le variazioni di rendering dovute alla rotazione fanno parte dell'intervento di presentazione.
- Il riferimento sulla conservazione del lato è calcolato esternamente dal codice, con gli stessi due bridge già certificati. Nessuna tabella di copertura o verdetto sul candidato entra nelle richieste.

## Interpretazione limitata al controllo

In questa coppia l'ostacolo rimasto è respingere un bridge **formalmente ammissibile** che non soddisfa lo specifico requisito del lato intero sul bordo di una nuova regione. Il test non dimostra che gli ID siano irrilevanti: le probabilità variano con la rinomina, ma non abbiamo repliche o più permutazioni. Non dimostra neppure che l'orientazione sia irrilevante in generale: è stata provata una sola rotazione con riflessione fissa.

Un errore storico preselezionato, due bridge, una nuova orientazione e una biiezione non costituiscono otto geometrie indipendenti. Immagini e state restano insieme. Non si ricavano prove geometriche, spiegazioni del meccanismo interno, scoperta autonoma dei Generic Spaces o ragionamento sequenziale interno. La soglia .5 resta quella preregistrata: nessuna ricerca successiva di una soglia che migliori questo campione.

## Esecuzione e audit

- Branch dedicato `codex/right-pair-orientation-ids`, derivato da `cd751d03a0f416ccd27ec21f6091684b62e0a7f9`; `main` e gli esperimenti precedenti preservati.
- Pipeline live: **165 test e build riusciti**. Chiamate esclusivamente GitHub Actions con jev-1.14.0, secret del repository e header TypeSafe-Danger-Zone-Images: true. Nessun errore API, riparazione o domanda ripetuta.
- Audit offline: quattro richieste ricostruite, otto risposte native, 16 controlli dei contratti materiali e otto riferimenti ricontrollati. Invarianza esatta di state/domande dopo rinomina inversa; hash delle richieste e byte PNG congelati esatti.
- Test grafici: il renderer riproduce i pixel del baseline storico; a orientazione fissa la rinomina cambia solo i glifi. Distanze, topologia, chiralità e centro conservati dalla rotazione. Le sole quantità numeriche rigenerate ammettono tolleranza 1e-12 nell'audit; risposte e hash non vengono arrotondati.
- Usage: **13,428 input token e 168 output token**. Total_tokens non restituito, lasciato null. Nessuna confidenza separata o affidabilità numerica restituita, campi null. Nessuna chiave o corpo d'errore negli artifact.

`live_results.json` conserva gli otto giudizi effettivi e il contesto storico separato. Il viewer offline confronta tutte le quattro versioni, compreso il negativo ancora errato. Protocollo e fixture manifest registrano la rotazione e la biiezione prima del live.
