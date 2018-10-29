import orodja

for i in range(1, 22):
    url = (
        r'https://www.avto.net/Ads/results.asp?znamka=Volkswagen&stran={}'
    ).format(str(i))
    orodja.shrani_spletno_stran(url, 'spletne-strani/stran-{}.html'.format(i))