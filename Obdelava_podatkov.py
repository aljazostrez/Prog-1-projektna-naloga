import re
import orodja

vzorec_bloka = re.compile(
    r'DESCRIPTION .*?'
    r'KOMENTAR CENE',
    flags=re.DOTALL
)


podatki_avtomobila = re.compile(
    r'<span>(?P<model>.*?)</span>.*?'
    r'<ul>.*?<li>(?P<letnik>.*?)</li>.*?'
    r'<li>(?P<gorivo>.*?) motor, (?P<prostornina_v_ccm>.*?) ccm, '
    r'(?P<moc_v_kW>.*?) kW\s*?/.*?KM</li><li>(?P<menjalnik>.*?)</li>.*?'
    r'REDNA OBJAVA CENE.*?'
    # Avtomobili, ki nimajo cene ('Pokličite za ceno') nas
    # ne zanimajo, zato vzamemo samo tiste, kjer je cena število.
    r'(?P<cena_v_evrih>(\d+\.)?\d+)',
    flags=re.DOTALL
)

kilometri = re.compile(
    r'<li>(?P<prevozeni_kilometri>[0-9]{0,7}) km</li><li>.*? motor',
    flags=re.DOTALL
)

def izloci_podatke_avtomobila(blok):
    try:
        avto = podatki_avtomobila.search(blok).groupdict()
        avto['model'] = avto['model'].split(' ')[1]
        # utf-8
        avto['model'] = avto['model'].replace('è', 'č')
        avto['model'] = avto['model'].replace('', 'š')
        # če avto ni nov, a vseeno nima napisanih kilometrov,
        # ga za našo analizo podatkov izpustimo.
        if 'NOVO' in avto['letnik']:
            avto['prevozeni_kilometri'] = 0
        else:
            avto['prevozeni_kilometri'] = int(
                kilometri.search(blok).group(1)
                )
        if 'registracije' in avto['letnik']:
            letnica = avto['letnik'][avto['letnik'].index(':')+1:]
            avto['letnik'] = int(letnica)
        else:
            avto['letnik'] = 2018
        avto['gorivo'] = avto['gorivo'].split(' ')[0]
        if 'bencin' in avto['gorivo']:
            avto['gorivo'] = 'bencin'
        else:
            avto['gorivo'] = 'dizel'
        avto['prostornina_v_ccm'] = int(avto['prostornina_v_ccm'])
        avto['moc_v_kW'] = int(avto['moc_v_kW'])
        if avto['menjalnik'][0] == 'r':
            avto['menjalnik'] = 'ročni'
        else:
            avto['menjalnik'] = 'avtomatski'
        if '.' in avto['cena_v_evrih']:
            avto['cena_v_evrih'] = avto['cena_v_evrih'].replace('.', '')
        avto['cena_v_evrih'] = int(avto['cena_v_evrih'])
        return avto
    except:
        # Če blok nima podatka o prevoženih km (in avto ni nov),
        # funkcija vrne None.
        return None


def avtomobili_na_strani(st_strani):
    ime_datoteke = 'spletne-strani/stran-{}.html'.format(st_strani)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    avti = []
    for blok in vzorec_bloka.finditer(vsebina):
        avti.append(blok.group(0))
    return avti


avtomobili = []
for st_strani in range(1, 22):
    for avto in avtomobili_na_strani(st_strani):
        podatki = izloci_podatke_avtomobila(avto)
        if podatki:
            avtomobili.append(izloci_podatke_avtomobila(avto))

avtomobili.sort(key=lambda y: y['letnik'])

orodja.zapisi_csv(
    avtomobili, ['model', 'letnik', 'prevozeni_kilometri',
    'gorivo', 'prostornina_v_ccm', 'moc_v_kW', 'menjalnik',
    'cena_v_evrih'], 'obdelani-podatki/avtomobili.csv'
    )

orodja.zapisi_json(avtomobili, 'obdelani-podatki/avtomobili.json')