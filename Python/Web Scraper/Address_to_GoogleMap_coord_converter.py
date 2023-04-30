import googlemaps
from datetime import datetime

# Inizializza il client della Google Maps API
gmaps = googlemaps.Client(key='Insert Your Key')

# Indirizzo di cui si vogliono conoscere le coordinate
indirizzo = 'via Livia Drusilla, Cinecittà, Roma'

# Utilizza la funzione geocode() per ottenere le coordinate dell'indirizzo
geocode_result = gmaps.geocode(indirizzo)

# Stampa le coordinate dell'indirizzo
print(geocode_result[0]['geometry']['location'])
