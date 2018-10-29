import re

import orodja

vzorec_oglasa = re.compile(
    r'DESCRIPTION .*?'
    r'KOMENTAR CENE',
    flags=re.DOTALL
)

with open('stran-1.html', 'r') as dat:
    niz = dat.read()

l = []
for ujemanje in vzorec_oglasa.finditer(niz):
    oglas = ujemanje.group(0)
    if len(oglas) > 20000:
        # Problem je le prvi oglas. Da se izognemo
        # nadaljnih težav, ga takoj uredimo.
        oglas = oglas[26150:]
    l.append(oglas)

podatki_avtomobila = re.compile(
    r'<span>(?P<ime>.*?)</span>.*?'
    r'<ul>.*?<li>(?P<letnik>.*?)</li>.*?'
    r'<li>(?P<prevozeni_km>.*?)</li>.*?'
    r'<li>(?P<gorivo>.*?), (?P<prostornina>.*?), '
    r'(?P<moc>.*?) / .*?<li></li>(?P<menjalnik>.*?)</li>',
    #r' .*? </ul> .*?  REDNA OBJAVA CENE : \D*?'
    #r'(?P<cena>\d+ (\. \d+)?)',
    flags=re.DOTALL
)


avto = podatki_avtomobila.search(l[0]).groupdict()