import os.path
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

species_codes = []
species_common_name = {}
with open('ebird_taxa.csv', newline='', encoding='utf-8') as csvfile: # Species list here
    reader = csv.DictReader(csvfile)
    for row in reader:
        species_codes.append(row['species_code'])
        species_common_name[row['species_code']] = row['common_name']

headers = {
    'Cookie': '', # Cookie here
    'Refer': 'https://birdsoftheworld.org/',
    'user_agent': '' # User agent here
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
            folder_path = os.path.join('test_ebird', common_name)
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
