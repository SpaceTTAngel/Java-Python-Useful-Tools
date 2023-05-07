import requests, lxml.html
import pandas as pd
import os


data = {key:[] for key in ['year','date','main','jolly','superstar']}
print(data)

#creazione dataframe vuoto
df=pd.DataFrame(data)

for year_int in range(2010, 2024):
    url = f'https://www.superenalotto.net/en/results/{year_int}'
    html = lxml.html.fromstring(requests.get(url).text)
    rows = html.xpath("//tbody/tr[not(@class)]")
    for row in rows:
        data['year'] = [str(year_int)]
        print( data['year'])
        data['date']  = [' '.join(row.xpath("./td[contains(@class,'date')]/text()"))]
        data['main']  = [row.xpath("./td[@class='ballCell'][1]//li/text()")]
        data['jolly'] = [row.xpath("./td[@class='ballCell'][2]//li/text()")[0]]
        data['superstar'] = [row.xpath("./td[@class='ballCell'][3]//li/text()")[0]]
        df = df.append(data, ignore_index=True) 


# Ottiene il percorso assoluto della directory corrente
dir_path = os.path.dirname(os.path.realpath(__file__))

# Salva il DataFrame in un file Excel nella directory corrente
file_path = os.path.join(dir_path, "estratti_superenalotto_option2.xlsx")
df.to_excel(file_path, index=False)