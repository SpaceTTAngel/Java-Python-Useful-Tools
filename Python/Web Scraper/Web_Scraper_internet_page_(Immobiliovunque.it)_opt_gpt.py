import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os


def get_apartment_info(url):
    """
    Estrae le informazioni degli appartamenti da una pagina web.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    apartment_link_vector=[]
    apartment_title_vector=[]
    apartment_price_vector=[]
    apartment_surface_vector=[]
    
    link_web_apartment_tags = soup.select('a.listing-area-nasty-lazy-links.m-2')
    for link in link_web_apartment_tags:
        apartment_link = link['href']
        apartment_link_vector.append(apartment_link)
        apartment_title = link.text.strip()
        apartment_title_vector.append(apartment_title)

    price_tags = soup.select('div.listing-price.flex-grow-1.d-flex')
    for price_tag in price_tags:
        price_text = price_tag.text.strip()
        apartment_price = price_text if '€' in price_text else '*'
        apartment_price_vector.append(apartment_price)

    surface_tags = soup.select('div.d-flex.area-room-container.p-2.mt-2.mt-lg-3')
    for surface_tag in surface_tags:
        surface_text = surface_tag.get_text(strip=True)
        apartment_surface = re.search(r'\d+\s*m²', surface_text).group() if 'm²' in surface_text else '*'
        apartment_surface_vector.append(apartment_surface)

    return apartment_link_vector, apartment_title_vector, apartment_price_vector, apartment_surface_vector


url_vector = [f"https://www.immobiliovunque.it/vendita-appartamenti/roma?page={i}&items=20&areas=appio-claudio%2Ccinecitta-don-bosco%2Ccinecitta-est%2Ccinecitta-lamaro" for i in range(1, 15)]
data = {'Link Appartamento': [], 'Titolo Appartamento': [], 'Prezzo Appartamento': [], 'Metri quadri appartamento': []}

for url in url_vector:
    print(url)
    apartment_link_vector, apartment_title_vector, apartment_price_vector, apartment_surface_vector = get_apartment_info(url)
    data['Link Appartamento'].extend(apartment_link_vector)
    data['Titolo Appartamento'].extend(apartment_title_vector)
    data['Prezzo Appartamento'].extend(apartment_price_vector)
    data['Metri quadri appartamento'].extend(apartment_surface_vector)

df = pd.DataFrame(data)
excel_filename = 'output_Main.xlsx'
df.to_excel(excel_filename, index=False)
