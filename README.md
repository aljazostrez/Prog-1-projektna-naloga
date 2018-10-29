# Analiza novih in rabljenih avtomobilov

Analiziral bom 1000 novih in rabljenih avtomobilov znamke Volkswagen na spletni 
strani [avto.net](https://www.avto.net/Ads/results.asp?znamka=Volkswagen), kjer se
vsakodnevno objavi več sto avtomobilskih oglasov. Zajel sem le podatke z oglasov,
ki imajo napisano ceno.

Za vsak avtomobilski oglas bom zajel:
* vrsto avtomobila
* letnik 1. registracije
* število opravljenih kilometrov
* vrsta goriva
* prostornina in moč motorja
* vrsta menjalnika
* cena

Delovne hipoteze:
* Kako avtomobilom pada cena v primerjavi z opravljenimi kilometri oz. letnikom?
* Katera vrsta avtomobila najbolje ohranja ceno glede na leto?
* Glede na oglase, ali lahko napovemo, s katerim avtomobilom bomo lahko naredili
največ kilometrov?
* Kateri avtomobili so bili najbolj popularni v določenih letih, tj. katerih
avtomobilov je bilo določenega leta največ?

V mapi spletne-strani so html-ji vseh spletnih strani, iz katerih smo črpali podatke. Podatke smo zajeli s pomočjo skripte Zajem_podatkov.py, obdelali pa s pomočjo skripte Obdelava_podatkov.py. S to skripto in modulom orodja.py smo izdelali datoteki *.csv in *.json. V mapi obdelani-podatki sta datoteki avtomobili.csv, ki vsebuje tabelo z naslednjimi vrednostmi:
* model (avtomobila)
* letnik
* prevozeni_kilometri (Prevoženi kilometri)
* gorivo (vrsta goriva)
* prostornina_v_ccm (Prostornina \[ccm\])
* moc_v_kW (Moč \[kW\])
* menjalnik (vrsta menjalnika)
* cena_v_evrih (cena \[€\])
in datoteka avtomobili.json z istimi vrednostmi.