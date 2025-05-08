import requests
import json



def get_stations_around(latitude: float, longitude: float) -> dict:

    url = f"https://api.prix-carburants.2aaz.fr/stations/around/{latitude},{longitude}"
    params = {
        "types": "R,A",
        "responseFields": "Hours,Fuels",
    }
    headers = {
        "Accept": "application/json",
        "Range": "station=1-5"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None


def get_fuel_price(fuels: list, fuel_type: str) -> dict:
    for fuel in fuels:
        if fuel["short_name"] == fuel_type:
            return fuel
    return None



def main():
    
    fuel_type = "SP98"
    
    print("Chargement des stations autour de chez vous...")
    stations = get_stations_around(48.785588, 2.246038)
    
    if stations:
        for station in stations:
            print("\n" + "="*50)
            print(f"Station: {station['Brand']['name']}")
            print(f"Adresse: {station['Address']['street_line']}, {station['Address']['city_line']}")
            print(f"Distance: {station['Distance']['text']}")
            
            fuel = get_fuel_price(station["Fuels"], fuel_type)
            print(fuel)
            if fuel and "Price" in fuel:
                print(f"Prix {fuel_type}: {fuel['Price']}€/L")
            else:
                print(f"{fuel_type} non disponible")

if __name__ == "__main__":
    main() 