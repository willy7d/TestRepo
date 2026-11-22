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

## v2 (22/11) – camminata su curve normative
Cosa rendeva falso il movimento della v1: passo troppo corto (280 unità contro le ~380 della posa di contatto disegnata), ginocchio quasi rigido in swing, gamba d'appoggio sempre tesa, braccia quasi ferme, ritagli sfumati, arresto a gambe divaricate con dissolvenza.

Cosa è cambiato:
- **Motore** (`template.html`): tabelle al 5 % del ciclo per angolo coscia, flessione ginocchio e caviglia (forma e tempi da Winter 1991 / Perry 1992, valori trascritti a memoria: non un dataset importato). Appoggio 62 %, pianta a terra al 10 %, stacco del tallone al 36 %. Il piede d'appoggio rotola senza strisciare (tallone → pianta → avampiede/punta); l'altezza del bacino è risolta perché il ginocchio in appoggio segua la curva normativa (oscillazione ~7,6 unità, minimo in doppio appoggio); lo swing è la cinematica diretta delle curve, raccordata ai contatti. Falcata 385 e appoggio 86 scelti con `tools/fit.js` minimizzando lo scarto dalle curve (RMS ginocchio 4,9°, coscia 3,3°). Slittamento del piede a terra: 0 (misurato).
- Braccia in opposizione con gomito che si flette in avanti, leggera controrotazione bacino/spalle, busto quasi fermo.
- Busto in camminata inclinato in avanti di 7,5° e portato 9 unità più avanti rispetto alle anche (`LEAN`, `FWD` in `template.html`); torna dritto quando si ferma. Corregge il «busto troppo indietro e dritto» segnalato dall'utente.
- **Arresto e ripartenza**: decelera, passo di chiusura a piedi uniti, giro "a carta" (senza dissolvenza semitrasparente), fumetto 3 s, giro, primo passo dalla posizione ferma.
- **Ritagli** (`tools/cut2.py`, `tools/legpoly.py`): coscia, tibia e stivale rifatti dalla gamba d'appoggio della posa 4 (dritta e tutta visibile), bordi netti, calotta tonda al ginocchio → niente più ginocchio gonfio. Busto e braccia restano quelli della v1.
- Anteprime rigenerate: `preview/Lexia-anteprima.mp4` (H.264, 1280×480, 30 fps, 14 s), `preview/big.png` (8 fasi), `preview/sheet.png` (fotogrammi del video).

Limiti rimasti: il giro verso chi guarda non è una vera rotazione (manca una posa di tre quarti); bordo del braccio vicino ancora un po' frastagliato; ginocchio della gamba arretrata che si flette un po' prima della curva normativa (50–55 % del ciclo); verificato su Chromium (desktop, emulazione iPhone 13, reduced-motion), non su Safari reale.

Strumenti v2 (da una cartella di lavoro con `src/p4.png` = cella 4 dello sprite, `parts/`, `template.html`, `rig.json`): `cut2.py` → parti gamba + `rig.json`; `build.py [out.html] [S=… C=…]`; `dbg.js` angoli per fase contro le curve; `fit.js` ricerca S/C; `seq.js` foglio di fotogrammi della sequenza; `rec.js` fotogrammi per l'MP4 (`ffmpeg -framerate 30 -i frames/f%04d.png -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -movflags +faststart`).
