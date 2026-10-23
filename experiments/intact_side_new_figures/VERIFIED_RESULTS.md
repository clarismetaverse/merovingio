# Richiesta esplicita su figure nuove: 10/12, trasferimento parziale

**La richiesta esplicita funziona su due nuove figure, ma sbaglia una coppia del rettangolo.** Il precedente 6/6 sullo stesso host isoscele non si trasferisce perfettamente a questi casi. Questo esperimento contiene tre host nuovi e sei coppie di bridge vicini, senza tabella di copertura nell'input di Jev.

Il [run live 39994076040](https://github.com/clarismetaverse/merovingio/actions/runs/39994076040) è concluso con successo, commit `89cea8410acef74f276f5d94fb9bf65f2b083f8a`. **Tre richieste, quattro Noul ciascuna: 12 giudizi totali, nessun retry, Score o composito.** Testo dell'obiettivo, policy generale e domanda binaria sono identici al precedente controllo explicit. Ogni candidato soddisfa entrambi i contratti locali storici dei Generic Spaces; solo il codice determina il riferimento e lo mantiene fuori dal payload.

| Figura | Corretti | TP | FN | TN | FP | Astensioni | Brier medio |
|---|---:|---:|---:|---:|---:|---:|---:|
| Scaleno acutangolo | 4/4 | 2 | 0 | 2 | 0 | 0 | .150575 |
| Scaleno rettangolo | 2/4 | 1 | 1 | 1 | 1 | 0 | .242050 |
| Scaleno ottusangolo | 4/4 | 2 | 0 | 2 | 0 | 0 | .117725 |
| Totale | **10/12** | **5** | **1** | **5** | **1** | **0** | **.170117** |

La soglia preregistrata è invariata: p>.5 sì, p<.5 no; p=.5 astensione contata errata. Sempre sì o sempre no darebbero 6/12 su questo campione bilanciato. Le probabilità sono spesso vicine alla soglia: la correttezza del singolo giudizio non equivale a certezza o robustezza su nuove presentazioni.

## Tutte le probabilità native

| Figura | Candidato | Riferimento esterno | P(sì) Jev | Esito |
|---|---|---|---:|---|
| Acutangolo | C606 | sì | .63 | corretto |
| Acutangolo | C346 | no | .42 | corretto |
| Acutangolo | C982 | sì | .61 | corretto |
| Acutangolo | C280 | no | .37 | corretto |
| Rettangolo | C117 | sì | .52 | corretto |
| Rettangolo | C320 | no | .36 | corretto |
| Rettangolo | C914 | sì | .41 | falso negativo |
| Rettangolo | C850 | no | .51 | falso positivo |
| Ottusangolo | C367 | sì | .67 | corretto |
| Ottusangolo | C743 | no | .38 | corretto |
| Ottusangolo | C592 | sì | .76 | corretto |
| Ottusangolo | C300 | no | .40 | corretto |

Cinque coppie su sei hanno entrambi i giudizi corretti e P(sì)_positivo > P(sì)_negativo. La coppia errata è C914/C850 nel rettangolo: **.41 contro .51**, margine −.10. Qui non c'è soltanto un attraversamento della soglia: anche l'ordine delle probabilità è invertito. Nell'altra coppia del rettangolo il positivo C117 è appena sopra soglia (.52).

Le costruzioni vicine restano formalmente ammissibili. Nella coppia errata, il positivo parte da un endpoint originale del lato designato e raggiunge un punto vicino al vertice opposto; il negativo parte dal vertice opposto e termina dentro il lato designato vicino a quell'endpoint. Entrambi i tagli sono vicini allo stesso bordo originale. Il primo lascia tutto il lato designato sul bordo di una regione, il secondo lo divide. Gli spostamenti massimi degli endpoint abbinati nelle sei coppie sono 18.70–29.16 pixel e non superano la frazione preregistrata .10/.12/.14 del lato più lungo del rispettivo host.

## Interpretazione

La formulazione esplicita riduce l'ambiguità della richiesta e si trasferisce a diversi casi nuovi, ma non garantisce l'applicazione corretta del predicato a ogni workspace. Non possiamo attribuire l'errore all'angolo retto: forma, rotazione/riflessione e alias non sono incrociati in questo piccolo run. Le sottofigure sottili e i tagli vicini al bordo sono intenzionali; non abbiamo isolato il contributo della lettura visiva rispetto ai cicli e alle relazioni strutturate forniti insieme.

Tutti i bridge sono validi per entrambi i GS, quindi il falso positivo non è un binding materialmente invalido accettato. È un candidato ammissibile che non soddisfa lo specifico requisito del lato intatto. Il modello riceve immagini, region_vertex_cycles, certificati materiali e fatti metrici preesistenti; non riceve intervalli/frazioni o la tabella di copertura dei lati, né un'etichetta di utilità del candidato.

Tre geometrie con quattro tagli ciascuna e sei coppie correlate non sono dodici campioni indipendenti. Il precedente 6/6 explicit è solo confronto storico: niente controllo contemporaneo sul vecchio host e niente conclusione causale sullo scoring. Nessuna calibrazione delle probabilità, prova geometrica, pertinenza aperta, scoperta autonoma dei Generic Spaces o ragionamento sequenziale interno viene dimostrato.

## Esecuzione, sicurezza e riproducibilità

- Branch: `codex/intact-side-new-figures`, derivato da `b3fdbbf1b4985489995bce685958e5eab5aaa714`; `main` e tutti gli esperimenti precedenti preservati.
- Pipeline live: **151 test e build riusciti**, tre richieste solo via GitHub Actions, modello jev-1.14.0, repository secret e header TypeSafe-Danger-Zone-Images: true. Nessun errore API o richiesta ripetuta.
- Audit offline: tre richieste ricostruite, 12 risposte verificate, 24 controlli dei contratti materiali, 12 riferimenti geometrici e sei relazioni di vicinanza ricontrollati. Byte PNG e hash delle richieste sono esatti; solo quantità rigenerate ammettono tolleranza 1e-12 fra Python 3.11/3.12.
- Il manifest delle fixture usa la rappresentazione testuale LF di Git per rendere l'hash indipendente dai fine-riga Windows. Il digest registrato dal runner coincide con quello del blob Git. Questa correzione dell'audit locale non cambia alcun input, PNG o risposta e non richiede nuove chiamate.
- Usage complessivo: **15,509 input token, 240 output token**; total_tokens non restituito e lasciato null. Nessuna affidabilità o confidenza separata numerica restituita; campi null. Noul è la probabilità nativa di sì, non un grado di pertinenza.
- `live_results.json` conserva le risposte sanificate effettive. `observer_only_coverage` nei risultati è evidenza per l'audit: non è mai entrata nel model_input o nel corpo delle richieste.

Il viewer offline affianca figure, riferimenti esterni e probabilità. Protocollo e manifest congelano casi e criteri prima del live. Il test non è una sequenza temporale: le immagini sono costruzioni alternative.
