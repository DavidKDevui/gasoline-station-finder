import requests
import json
from datetime import datetime
import geocoder


JOURS_FR = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche"
}



def get_current_location():

    g = geocoder.ip('me')
    if g.ok:
        return g.lat, g.lng
    return None


def get_stations_around(latitude: float, longitude: float) -> dict:

    url = f"https://api.prix-carburants.2aaz.fr/stations/around/{latitude},{longitude}?types=R,A&responseFields=Fuels,Hours"
 
    headers = {
        "Accept": "application/json",
        "Range": "station=1-5"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None



def get_station_hours(days: list, current_day: str) -> dict:
    for day in days:
        if day["name"] == current_day:
            return day["TimeSlots"][0]
    return None

 


def main():
    
    #fuel_type = "SP98"
    print("\nChargement des 5 stations les plus proches de chez vous...")
    
    location = get_current_location()
    if location:
        lat, lng = location
        #print(f"Votre position : {lat}, {lng}")
        stations = get_stations_around(lat, lng)
    else:
        print("Impossible de détecter votre position, utilisation des coordonnées par défaut (Paris)")
        return
    
    current_day = JOURS_FR[datetime.now().strftime("%A")]

    if stations:
        for station in stations:
            open_hours = get_station_hours(station['Hours']['Days'], current_day)
            
            print("\n" + "="*50)
            print(f"Station: {station['Brand']['name']}")
            print(f"Adresse: {station['Address']['street_line']}, {station['Address']['city_line']}")
            print(f"Distance: {station['Distance']['text']}")
            
            if open_hours:
                print(f"Ouvert aujourd'hui de {open_hours['opening_time']} à {open_hours['closing_time']}")
            else:
                print("Pas d'informations sur les horaires")
    else:
        print("Aucune station trouvée")
        
    print("")

if __name__ == "__main__":
    main() 
