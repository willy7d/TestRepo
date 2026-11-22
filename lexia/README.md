# Lexia – camminata del widget di assistenza (passaggio di consegne)

## Obiettivo (brief originale, Slack #ai-agents, 21/11)
Lexia a figura intera cammina in fondo alla pagina con andatura umana credibile:
- ciclo continuo tallone → pianta → punta, trasferimento del peso, braccia in opposizione, piedi fermi a terra, passo moderato, testa/busto quasi fermi, nessun salto al riavvio;
- entra da sinistra, rallenta vicino al lato destro, ruota verso chi guarda, si ferma, fumetto HTML «Se hai bisogno, dimmi!» ~3 s, riparte;
- fondo trasparente, controlli della pagina liberi, prefers-reduced-motion = posa ferma + fumetto;
- desktop + Safari iPhone; consegna demo web + anteprima animata apribile da telefono.
- Design da conservare: volto, capelli scuri, camicia prugna, pantaloni e stivaletti scuri, posa frontale.

## Cosa è stato fatto (v1)
- `src/sprite-sei-pose.png`: sprite 3×2 trasparente (estratto dalla demo originale). `src/posa-frontale.png`: posa frontale trasparente.
- Rig 2D a ritaglio dalla posa in alto a sinistra (512×512): corpo (braccia rimosse + inpainting OpenCV), braccio (omero/avambraccio), coscia, tibia, stivale. Un solo template per gamba/braccio, il lato lontano è scurito.
- Animazione procedurale su canvas (`template.html` → `build.py` inietta `rig.json` → `Lexia-camminata.html`):
  IK a due ossa, piede in appoggio bloccato al suolo, rollio tallone/pianta/punta, swing con curva min-jerk, altezza bacino dal vincolo della gamba d'appoggio, fase legata alla distanza (niente scivolamento), decelerazione/accelerazione di un passo, rotazione = dissolvenza con schiacciamento orizzontale verso la posa frontale.
- Anteprime: `preview/Lexia-anteprima.mp4`, `preview/big.png` (4 fasi), `preview/sheet.png` (fotogrammi della sequenza).
- Strumenti (`tools/`, si lanciano da una cartella di lavoro con `src/img0.png`, `src/img1.png`, `parts/`): `cut.py` ritaglia le parti, `export.py` crea `rig.json`, `build.py`, `strip.js` / `shots.js` / `rec.js` (Playwright) per fotogrammi e video, `dbg.js` stampa altezza bacino e flessione ginocchio per fase.

## Giudizio dell'utente
«Meglio ma ancora non va bene.» Problemi noti:
- curve articolari inventate (non da dati reali) → movimento poco credibile;
- ginocchio "gonfio" quando la gamba in swing si piega molto (giunzione coscia/tibia del ritaglio);
- rotazione verso chi guarda = dissolvenza, non vera rotazione;
- testato solo su Chromium (anche emulazione iPhone 13), non su Safari reale.

## Strade valutate
1. Pilotare il rig con curve di gait reali (angoli sagittali normativi anca/ginocchio/caviglia, es. dati di Winter; tempi di appoggio/swing e oscillazione bacino reali) + migliorare le giunzioni del ritaglio.
2. Modello 3D di Lexia (image-to-3D, es. Meshy/Tripo) → camminata mocap Mixamo → render sprite 2D da Blender (rischio somiglianza; richiede account dell'utente).
3. Animatore professionista (Spine o frame a mano).
