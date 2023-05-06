import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# crea un dataframe vuoto per i dati estratti
df = pd.DataFrame(columns=['anno', 'data', '1°', '2°', '3°', '4°', '5°', '6°', 'Jolly', 'Superstar','concorso'])

# loop su tutti gli anni dal 1871 al 2023
for year in range(1871, 2024):

    # costruisce l'URL della pagina web per l'anno corrente
    url = f'https://www.franknet.altervista.org/superena/{year}.HTM'
    print(url)

    # scarica il contenuto della pagina web
    response = requests.get(url)

    # crea un oggetto BeautifulSoup per il parsing del contenuto HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    #print(soup)

    # estrae la tabella dei dati
    table = soup.find_all('pre', {'style': 'border-style: ridge'})
    #print(table)

    # estrae i dati della tabella e li aggiunge al dataframe principale
    for pre in table:
        rows = pre.get_text().split("\n")
        #print(rows)
        for row in rows:
            cols = row.split()
            #print(cols)
            #if cols[0] != str(year):
                #print(" ".join(cols))
            if cols and cols[0] != str(year) and len(cols)==11:
                # siamo in presenza di una riga dati
                year = year
                #print(year)
                day = cols[0] + ' ' + cols[1]
                #print(day)
                estratti = cols[2:8]
                estratto_1=cols[2]
                estratto_2=cols[3]
                estratto_3=cols[4]
                estratto_4=cols[5]
                estratto_5=cols[6]
                estratto_6=cols[7]
                #print(estratti)
                jolly = cols[8]
                #print(jolly)
                superstar = cols[9]
                #print(superstar)
                concorso = cols[10]
                #print(concorso)
                data = {'anno': year,
                        'data': day,
                        '1°' : estratto_1,
                        '2°' : estratto_2,
                        '3°' : estratto_3,
                        '4°' : estratto_4,
                        '5°' : estratto_5,
                        '6°' : estratto_6,
                        'Jolly': jolly,
                        'Superstar': superstar,
                        'concorso': concorso}
                df = df.append(data, ignore_index=True)  
                      
            if cols and cols[0] != str(year) and len(cols)==10:
                # siamo in presenza di una riga dati
                year = year
                #print(year)
                day = cols[0] + ' ' + cols[1]
                #print(day)
                estratti = cols[2:8]
                estratto_1=cols[2]
                estratto_2=cols[3]
                estratto_3=cols[4]
                estratto_4=cols[5]
                estratto_5=cols[6]
                estratto_6=cols[7]
                #print(estratti)
                jolly = cols[8]
                #print(jolly)
                concorso = cols[9]
                #print(concorso)
                data = {'anno': year,
                        'data': day,
                        '1°' : estratto_1,
                        '2°' : estratto_2,
                        '3°' : estratto_3,
                        '4°' : estratto_4,
                        '5°' : estratto_5,
                        '6°' : estratto_6,
                        'Jolly': jolly,
                        'Superstar': '--',
                        'concorso': concorso}
                df = df.append(data, ignore_index=True)     


# Ottiene il percorso assoluto della directory corrente
dir_path = os.path.dirname(os.path.realpath(__file__))

# Salva il DataFrame in un file Excel nella directory corrente
file_path = os.path.join(dir_path, "estratti_superenalotto.xlsx")
df.to_excel(file_path, index=False)
