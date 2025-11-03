import os.path
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

species_codes = []
species_common_name = {}
with open('/Users/tangerine/Documents/ebird_taxa.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        species_codes.append(row['species_code'])
        species_common_name[row['species_code']] = row['common_name']

headers = {
    'Cookie': 'i18n_redirected=en; _gcl_au=1.1.2001593028.1726221630; _ga=GA1.3.321248097.1726221631; hubspotutk=097d724964eb8a59a5551aaf533098c7; ml-search-session=eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVIxNzgyOTAzIiwidXNlcm5hbWUiOiJaaGVqaWFuZ2ZhdW5hIiwiZmlyc3ROYW1lIjoiWmhlamlhbmciLCJsYXN0TmFtZSI6IkZhdW5hIiwiZnVsbE5hbWUiOiJaaGVqaWFuZyBGYXVuYSIsInJvbGVzIjpbXSwicHJlZnMiOnsiUFJJVkFDWV9QT0xJQ1lfQUNDRVBURUQiOiJ0cnVlIiwiU0hPV19TVUJTUEVDSUVTIjoidHJ1ZSIsIkRJU1BMQVlfTkFNRV9QUkVGIjoibiIsIlZJU0lUU19PUFRfT1VUIjoiZmFsc2UiLCJESVNQTEFZX0NPTU1PTl9OQU1FIjoidHJ1ZSIsIkRJU1BMQVlfU0NJRU5USUZJQ19OQU1FIjoidHJ1ZSIsIlNIT1dfQ09NTUVOVFMiOiJmYWxzZSIsIkNPTU1PTl9OQU1FX0xPQ0FMRSI6InpoX1NJTSIsIkdNQVBfVFlQRSI6Imh5YnJpZCIsIkFMRVJUU19PUFRfT1VUIjoiZmFsc2UiLCJFTUFJTF9DUyI6InRydWUiLCJUT1AxMDBfT1BUX09VVCI6ImZhbHNlIiwiRElTVF9VTklUIjoia20iLCJzcHBQcmVmIjoiYm90aCJ9fX0=; ml-search-session.sig=_lNDhBQq3xUjxyE47SNBn0EbJAU; _gid=GA1.2.887724427.1733724627; _gid=GA1.3.887724427.1733724627; _d0371=4114b5617d8b3823; _ga_QR4NVXZ8BM=GS1.1.1733816663.82.0.1733816663.60.0.0; _ga_CYH8S0R99B=GS1.1.1733816663.82.0.1733816663.60.0.0; _ga_YT7Y2S4MBX=GS1.1.1733816663.81.0.1733816663.0.0.0; _ga_DTHTPXK4V9=GS1.1.1733816663.82.0.1733816663.0.0.0; _ga=GA1.2.321248097.1726221631; __hstc=264660688.097d724964eb8a59a5551aaf533098c7.1726221639873.1733804876763.1733816665273.66; __hssrc=1; __hssc=264660688.1.1733816665273',
    'Refer': 'https://birdsoftheworld.org/',
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

for species_code in species_codes:
    url = f'https://search.macaulaylibrary.org/api/v2/search?taxonCode={species_code}&mediaType=photo&sort=rating_rank_desc'
    r = requests.get(url, headers=headers, timeout=300, verify=False)
    res = requests.get(url, headers=headers, timeout=300)
    b = res.json()
    lists = []
    for i in b:
        z = i.get('assetId')
        # print(z)
        lists.append(z)
        if len(lists) >= 5:
            break

    for j in lists:
        print(j)
        url = f'https://macaulaylibrary.org/asset/{j}'
        r = requests.get(url, headers=headers, timeout=300, verify=False)
        soup = bs(r.content, "html.parser")
        img = soup.findAll('img', attrs={'src': True})
        img_url = str(img[2]).split('src="')[1].split('" srcset')[0]
        print(img_url)

        if not img_url.endswith('/1200'):
            continue

        try:
            common_name = species_common_name.get(species_code, 'Unknown_Species')
            folder_path = os.path.join('/Users/tangerine/Desktop/test_ebird', common_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            save_path = os.path.join(folder_path, f"{j}.jpeg")

            if os.path.exists(save_path):
                print("file exists")
                continue

            print(save_path)
            urlretrieve(img_url, save_path)
        except Exception as e:
            print(f"download fail:{e}")
