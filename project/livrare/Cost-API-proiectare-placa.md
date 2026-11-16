# Astra A · costul API estimat pentru proiectarea plăcii

**454,66 USD** la tarifele GPT-6 Astra Standard consultate la 15 noiembrie 2026, presupunând același model și aceeași reutilizare a contextului. Estimarea acoperă proiectarea electronicii până la închiderea primului obiectiv, în 2.440 de apeluri ale agentului principal și ale celor opt subagenți. Carcasa aparține unui obiectiv ulterior. [Tarifele oficiale GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)

| Categorie | Tokeni | USD / milion | Cost estimat |
|---|---:|---:|---:|
| Intrări noi | 3.866.385 | 10,00 | 38,66 USD |
| Ieșire generată, inclusiv raționament | 952.948 | 50,00 | 47,65 USD |
| Intrări recitite din cache | 368.347.392 | 1,00 | 368,35 USD |
| **Total** | **373.166.725** | | **454,66 USD** |

**Cei 4.819.333 de tokeni ai contorului de obiectiv costă 86,31 USD.** Ei însumează intrările noi și ieșirea generată. Refolosirea instrucțiunilor, a conversației și a rezultatelor anterioare explică cele 368.347.392 de citiri din cache. Acestea reprezintă 81,02% din costul estimat. Din cei 952.948 de tokeni de ieșire, 279.656 sunt de raționament și sunt deja cuprinși în cei 47,65 USD. Sesiunile au înregistrat zero tokeni de scriere în cache, iar cea mai lungă intrare a avut 245.316 tokeni, sub pragul de 272.000 pentru context lung. [Procesarea și tarifele de cache](https://developers.openai.com/api/docs/models/gpt-6-astra)

## Defalcare pe activitate

Fiecare rând include intrările noi, citirile din cache și ieșirea agentului respectiv. Activitatea este atribuită după rolul agentului. Sumele pe rând sunt rotunjite la doi zecimali.

| Activitate | Apeluri | Tokeni noi + ieșire | Cost estimat cu cache |
|---|---:|---:|---:|
| Coordonare, integrare în Fusion și livrare | 576 | 722.046 | 101,46 USD |
| Fabricație, asamblare și verificări CAM | 304 | 582.193 | 57,81 USD |
| Plasare și rutare PCB | 302 | 645.888 | 53,55 USD |
| Audit independent | 270 | 680.023 | 51,38 USD |
| Alimentare solară, USB și baterie | 252 | 528.850 | 48,96 USD |
| Afișaj e-paper | 227 | 548.859 | 46,60 USD |
| Radio și antenă | 230 | 475.297 | 40,67 USD |
| Firmware | 148 | 281.471 | 28,00 USD |
| Trezire, RTC și senzori | 131 | 354.706 | 26,22 USD |
| **Total** | **2.440** | **4.819.333** | **454,66 USD** |

Calculul reprezintă contravaloarea tokenilor înainte de TVA. Instrumentele API cu tarif separat pot adăuga costuri pe apel. [Tarife pentru instrumente](https://developers.openai.com/api/docs/pricing#tools)
