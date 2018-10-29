import re

import orodja

vzorec_bloka = re.compile(
    r'DESCRIPTION .*?'
    r'KOMENTAR CENE',
    flags=re.DOTALL
)

#with open('stran-1.html', 'r') as dat:
#    niz = dat.read()
#
#l = []
#for ujemanje in vzorec_bloka.finditer(niz):
#    oglas = ujemanje.group(0)
#    if len(oglas) > 20000:
#        # Problem je le prvi oglas. Da se izognemo
#        # nadaljnih težav, ga takoj uredimo.
#        oglas = oglas[26150:]
#    l.append(oglas)

podatki_avtomobila = re.compile(
    r'<span>(?P<model>.*?)</span>.*?'
    r'<ul>.*?<li>(?P<letnik>.*?)</li>.*?(<li>(?P<prevozeni_kilometri>.*?) km</li>)?'
    r'<li>(?P<gorivo>.*?), (?P<prostornina_v_ccm>.*?) ccm, '
    r'(?P<moc_v_kW>.*?) kW\s*?/.*?KM</li><li>(?P<menjalnik>.*?)</li>.*?'
    r'REDNA OBJAVA CENE.*?'
    r'(?P<cena_v_evrih>(\d+\.)?\d+)',
    flags=re.DOTALL
)


def izloci_podatke_avtomobila(blok):
    try:
        avto = podatki_avtomobila.search(blok).groupdict()
        avto['model'] = avto['model'].split(' ')[1]
        if 'registracije' in avto['letnik']:
            letnica = avto['letnik'][avto['letnik'].index(':')+1:]
            avto['letnik'] = int(letnica)
        else:
            avto['letnik'] = 'NOVO'
        avto['prevozeni_kilometri'] = int(avto['prevozeni_kilometri'])
        avto['gorivo'] = avto['gorivo'].split(' ')[0]
        if 'bencin' in avto['gorivo']:
            avto['gorivo'] = 'bencin'
        else:
            avto['gorivo'] = 'dizel'
        avto['prostornina_v_ccm'] = int(avto['prostornina_v_ccm'])
        avto['moc_v_kW'] = int(avto['moc_v_kW'])
        if avto['menjalnik'][0] == 'r':
            avto['menjalnik'] = 'rocni'
        else:
            avto['menjalnik'] = 'avtomatski'
        if '.' in avto['cena_v_evrih']:
            avto['cena_v_evrih'] = avto['cena_v_evrih'].replace('.', '')
        avto['cena_v_evrih'] = int(avto['cena_v_evrih'])
        return avto
    except:
        return None


def avtomobili_na_strani(st_strani):
    ime_datoteke = 'stran-{}.html'.format(st_strani)
    niz = orodja.vsebina_datoteke(ime_datoteke)
    avtomobili = []
    for ujemanje in vzorec_bloka.finditer(niz):
        oglas = ujemanje.group(0)
        if len(oglas) > 20000:
            # Problem je le prvi oglas. Da se izognemo
            # nadaljnih težav, ga takoj uredimo.
            oglas = oglas[26150:]
        avtomobili.append(oglas)
    return avtomobili


avtomobili = []
for st_strani in range(1, 22):
    for avto in avtomobili_na_strani(st_strani):
        podatki = izloci_podatke_avtomobila(avto)
        if podatki != None:
            avtomobili.append(izloci_podatke_avtomobila(avto))

avtomobili.sort(key=lambda y: y['prevozeni_kilometri'])
orodja.zapisi_csv(
    avtomobili, ['model', 'letnik', 'prevozeni_kilometri',
    'gorivo', 'prostornina_v_ccm', 'moc_v_kW', 'menjalnik',
    'cena_v_evrih'], 'obdelani-podatki/avtomobili.csv'
    )
orodja.zapisi_json(avtomobili, 'obdelani-podatki/avtomobili.json')