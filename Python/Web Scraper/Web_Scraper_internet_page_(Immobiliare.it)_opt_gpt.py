import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL della pagina di ricerca immobiliare
url_start = "https://www.immobiliare.it/vendita-case/roma/?idMZona[]=10305&idMZona[]=10283&idQuartiere[]=12717"
url_vector = [url_start] + [f"https://www.immobiliare.it/vendita-case/roma/?pag={index_page}&idMZona[]=10305&idMZona[]=10283&idQuartiere[]=12717" for index_page in range(2, 45)]

apartment_title_vector, apartment_link_vector, apartment_price_vector, apartment_surface_vector = [], [], [], []

for url in url_vector:
    print(url)
    # Richiesta GET alla pagina web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Estrazione delle informazioni di interesse
    link_web_apartment_tags = soup.find_all('a', class_='in-card__title')
    price_tags = soup.find_all('li', class_='in-realEstateListCard__features--main')
    surface_tags = soup.find_all('li', class_="nd-list__item in-feat__item")

    #link appartamento e titolo
    for link in link_web_apartment_tags:
        apartment_title_vector.append(link['title'])
        apartment_link_vector.append(link['href'])
        
    #prezzo appartamento
    for price_tag in price_tags:
        price_text = price_tag.text.strip()
        if '€' in price_text:
            apartment_price_vector.append(price_text)
        else:
            apartment_price_vector.append('*')

    #metri quadri appartamento
    for surface_tag in surface_tags:
        surface_text = surface_tag.text.strip()
        if 'm²' in surface_text:
            apartment_surface_vector.append(surface_text)
    
# Crea un dizionario di dati con i tre vettori di stringhe
data = {'Link Appartamento': apartment_link_vector, 'Titolo Appartamento': apartment_title_vector, 'Prezzo Appartamento': apartment_price_vector, 'Metri quadri appartamento': apartment_surface_vector}

# Crea un DataFrame pandas con il dizionario di dati
df = pd.DataFrame(data)

# Ottieni il percorso della cartella corrente
current_path = os.getcwd()

# Aggiorna il nome del file Excel
excel_filename = 'output_Main.xlsx'

# Unisci il percorso della cartella corrente con il nome del file Excel
path = os.path.join(current_path, excel_filename)

df.to_excel(path, index=False)
print(f"Il file {excel_filename} è stato creato nella cartella corrente: {current_path}")