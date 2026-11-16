# Recepția direcțională a măștii J101

Eliberați subansamblul pentru presare când controlerul returnează **`release_pass = true`**. Verificarea include cele cinci contururi măsurate, centrajul, distanța axială film–metal și conul complet de vedere permis de carcasa calificată. În calculul de eliberare toate benzile adezive sunt transparente. [Programul de recepție](check_measured_profiles.py) · [Calculul proiecției](registered_optics.py) · [Carcasa și secțiunea PETG calificate](projection-datums.json)

## Măsurarea la comparator

1. Fixați J101 și laminatul în poziția de presare. Înregistrați identificatorii ansamblului, loturilor de conector, PET, adeziv, print și instrument, fotografiile calibrate și data. Axa X merge de la exterior spre PCB. Originea coordonatelor YZ din imagine poate fi centrul alezajului. Același reper rigid trebuie să apară în toate imaginile.
2. Exportați cinci contururi YZ în mm în liste de puncte închise, ordonate. `metal_bore` descrie gura prin care intră fișa, `metal_outer` exteriorul buzei metalice în planul său de sprijin, `pet_hole` decupajul fustei, `psa_hole` decupajul adezivului și `psa_outer` exteriorul adezivului cu urechi. Verificați ambele fețe ale tăieturii PET. Includeți în incertitudine conicitatea, bavurile, abaterea de interpolare dintre puncte și eroarea de înregistrare dintre planuri.
3. În `expanded_pairwise_uncertainty_mm` introduceți limita combinată a erorilor a două contururi înregistrate unul față de celălalt, la nivelul de acoperire documentat. Includeți scara, segmentarea, calibrarea și transferul poziției între imagini. Dacă bugetele sunt individuale, combinați-le conservator înainte de introducere. Limita admisă este 0,010 mm. O țintă de 0,003–0,005 mm simplifică potrivirea. Pe imaginile după presare, verificați poziția finală și repetați calculul dacă s-a deplasat filmul.
4. În `pet_back_to_steel_upper_mm` treceți distanța axială maximă dintre **spatele PET-ului opac** și planul buzei metalice, inclusiv incertitudinea și variația în jurul gurii. Nominal este 0,050 mm. Folosiți microscop cu focalizare calibrată, profilometru optic ori secțiune pe martor identic care limitează defensabil grosimea stratului, curl-ul și variația de presare a lotului. Măsurați ridicarea filmului la fiecare piesă. În exemple 0,055 mm este deja o limită superioară.
5. Legați fișa de revizia CAD în `case_step_sha256`. Verificați că secțiunea rigidă completă de la X = −8,750 mm închide traseul exterior și rămâne în fereastra de calibrare. Pe piesa de referință, lățimea pe Y este 17,120 mm. Coordonatele absolute pe Z sunt −4,395 și +5,820 mm. Abaterea în exterior a fiecărei muchii de print este maximum 0,250 mm pe axă. Centrul J101 raportat la reperul acestei secțiuni poate varia cu cel mult 0,350 mm pe fiecare axă Y și Z. Acest buget include originea optică de la `metal_bore`. Distanța axială măsurată între secțiune și planul metalic este cel puțin 8,400 mm. Includeți incertitudinile de poziționare și măsurare a carcasei în aceste limite. Înregistrați măsurările în fișa de lot și confirmați `pocket_within_projection_bounds = true` pentru exemplarele care le îndeplinesc. Identitatea CAD și fișa de calibrare fac parte din artefactele programului.

## Criterii

| Caracteristică după incertitudine | Limită |
|---|---:|
| Întregul alezaj metalic eliberat de fereastra PET | ≥0,025 mm |
| Retragerea muchiei adezivului față de PET | ≥0,010 mm |
| Lățimea continuă de contact între PSA și oțel | ≥0,035 mm |
| Excentricitatea radială a fustei față de alezaj | ≤0,035 mm |
| Distanța dintre proiecția tuturor razelor admise de fereastra PET și exteriorul oțelului | **≥0,005 mm** |

Primele trei limite înseamnă că alezajul poate fi dilatat cu 0,025 mm în interiorul PET-ului și că fereastra PET poate fi dilatată cu 0,045 mm în interiorul oțelului. Ultima valoare însumează retragerea de 0,010 mm și banda de 0,035 mm. La incidență oblică, o rază se poate depărta în spațiul axial dintre PET și metal. Verificarea din ultimul rând măsoară această deplasare pe fiecare direcție.

Pentru o rază care trece prin punctul `s` al secțiunii PETG și punctul `p` al deschiderii PET din spate, poziția la metal este `(1 + g/L)p − (g/L)s`. `g` este distanța film–metal, iar `L` este distanța secțiune–film, de cel puțin `8,400 − g` mm. Programul acoperă toate direcțiile simultan prin anvelopa convexă a ferestrei PET și cele patru colțuri ale dreptunghiului care include întreaga secțiune rotunjită PETG cu toleranțele de mai sus. În planul oțelului, măsoară distanța minimă de la această proiecție la conturul exterior real și scade `(1 + g/L) × U`, unde `U` este incertitudinea combinată. Protecția periferică a fustei are separat peste 1,251 mm pe Y și 0,710 mm pe Z la toleranțele carcasei. Ecranele interne J101 acoperă traseele care trec prin alezajul funcțional. Măsurările în STEP · Verificarea ecranelor J101

```sh
python check_measured_profiles.py specimen.json --suggest-recenter --output receptie.json
```

Codul de ieșire 0 înseamnă că măsurarea trece toate limitele. Codul 1 păstrează raportul și motivul respingerii. Lipsa distanței axiale, lipsa verificării locașului și altă revizie de carcasă lasă recepția în așteptarea măsurării sau recalificării. Păstrați scanările brute împreună cu fișierul de intrare și raportul.

## Corecția înainte de presare

Folosiți mai întâi deplasarea sugerată pe masa XY. Ea se referă la ansamblul PET și PSA înregistrat, văzut în axele Y și Z ale plăcii. Scanați din nou **toate cele cinci contururi reale**, cu placa fixată în noua poziție, apoi rulați din nou controlul. Grila de căutare are 0,005 mm și propune o poziție pentru verificare fizică. [Exemplul înainte de reglaj](examples/04-fail-before-recentering.json) · [Exemplul după reglaj](examples/05-pass-after-recentering.json)

Dacă pozițiile realizabile nu oferă margine suficientă, comandați un laminat nou. Pentru atelier, țintiți o tăietură cu **0,020 mm spre interior pe normală**, adică 8,64 × 2,86 mm R1,06, și centrare inițială radială ≤0,010 mm pe masa XY. Ținta rămâne în zona de toleranță de ±0,050 mm a desenului de serie. Convertorul pornește de la folie întreagă. O gaură deja prea mare necesită altă folie. Măsurați din nou epruveta, înregistrați-o la aceeași piesă J101 și verificați trecerea fișei, retragerea adezivului și banda de contact după toate cele cinci criterii. [DXF opțional de atelier la scara 1:1, în mm](examples/Optional-PET-target-minus-20um.dxf)

| Exemplu sintetic | Margine direcțională după incertitudine | Decizie |
|---|---:|---|
| 01, centrare (+0,004, −0,003), eroare PET +0,003, `U = 0,003` | +0,00566 mm | Acceptat |
| 02, centrare (+0,022, −0,022), eroare PET +0,020, `U = 0,002` | −0,03207 mm | Respins la proba oblică. Celelalte patru măsurări trec. |
| 03, același oțel, PSA și centrare ca la 02, PET nou la −0,020 | +0,00818 mm | Acceptat. Câștig de 0,04026 mm. |
| 04, înainte de recentrare | −0,00217 mm | Respins |
| 05, după deplasarea cu (−0,009, +0,004) mm a ansamblului de la 04 | +0,00591 mm | Acceptat în captura sintetică nouă |

Exemplul 03 păstrează 0,1260 mm la alezaj, 0,05199 mm față de PSA și 0,04631 mm de contact oțel–PSA, după incertitudine. Toate exemplele includ un spațiu axial maxim de 0,055 mm. [Intrarea 01](examples/01-pass-nonzero.json) · [Intrarea 02](examples/02-fail-oblique.json) · [Intrarea 03](examples/03-pass-recut-same-connector.json) · [Rezultate și coduri de ieșire pentru toate cele cinci exemple](examples/qualification-results.json)

## Probele pe lotul fizic

Fișa tesa descrie o peliculă centrală PET neagră și adeziv acrilic pe cele două fețe. Poziția stratului negru și transmisia optică laterală a straturilor subțiri de acrilic se stabilesc pe lot. Măsurați separat opacitatea celor două folii Toray și a benzii tesa pe martor. Verificați inelul opac și transferul de presiune pe întreg perimetrul. Pentru diagnostic se poate introduce `deepest_opaque_carrier_to_steel_upper_mm`, distanța maximă de la fața stratului negru dinspre oțel până la planul oțelului, incluzând eventuala zonă de aer și incertitudinea. Câmpul se obține prin secționarea unui martor sub presiunea de montare și inspecție optică pe lot. Raportul publică separat rezultatul ipotetic cu acest strat opac. Decizia `release_pass` folosește exclusiv proiecția PET–oțel cu toate PSA transparente. [Fișa tesa 68822](https://www.tesa.com/en/industry/tesa-68822.html)

Pe geometria sintetică 02, o rază trece la 0,00649 mm pe lângă conturul real al oțelului și lovește întâi FR4 la X = 1,47656, Y = 73,36595, Z = 0, cu PSA transparentă. Aceeași rază trece prin materialul inelului la o adâncime de 0,020 mm de oțel, dacă acolo există fizic stratul negru continuu. Cu această ipoteză suplimentară măsurată pe lot, marginea calculată pentru exemplul 02 este +0,0134 mm. Proba obligatorie cu toate PSA transparente păstrează verdictul de respingere. Proba geometrică a fost executată pe STEP. Pe primul articol fizic, fotografiați portul gol iluminat din spate cu aceeași expunere și martor deschis, verificați ambele orientări de mufare și repetați inspecția după cele 100 de cicluri din procedura de bază. [Raza și primul corp atins în BRep](examples/native-ray.json) · [Programul de reproducere](examples/verify_native_witness.py) · [Procedura de inspecție pe primul articol](README.md)
