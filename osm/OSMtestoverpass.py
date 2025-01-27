import requests
import json

def print_stations ():
    
    # Définissez votre requête Overpass pour obtenir les stations de métro dans une zone spécifique (par exemple, Paris)
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["name"="Paris"]->.searchArea;
    node["railway"="station"]["station"="subway"](area.searchArea);
    out body;
    """
    # Envoyer la requête
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Traitement des données
    for element in data['elements']:
        if 'name' in element['tags']:
            print(f"Station: {element['tags']['name']}, Location: ({element['lat']}, {element['lon']})")

def print_subway_lines ():
    pass

def print_subway (city):
    # URL de l'API Overpass
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Requête Overpass pour obtenir les lignes et les stations de métro dans une zone spécifique (exemple : Paris)
    overpass_query = f"""
    [out:json];
    area["name"="{city}"]->.searchArea;

    // Sélection des relations qui représentent les lignes de métro
    relation["route"="subway"](area.searchArea);
    out body;

    // Sélection des stations de métro
    node["railway"="station"]["station"="subway"](area.searchArea);
    out body;
    """
    print (overpass_query)
    # Envoi de la requête à Overpass
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Traitement des données pour afficher les lignes et les stations
    print("Lignes de métro :")
    for element in data['elements']:
        if element['type'] == 'relation' and 'name' in element['tags']:
            print(f" - Ligne: {element['tags']['name']}")

    print("\nStations de métro :")
    for element in data['elements']:
        if element['type'] == 'node' and 'name' in element['tags']:
            print(f" - Station: {element['tags']['name']}, Location: ({element['lat']}, {element['lon']})")

def print_subway_lines (city):
    
    # URL de l'API Overpass
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Requête Overpass pour obtenir les lignes de métro et les stations dans une zone (exemple : Paris)
    overpass_query = f"""
    [out:json];
    area["name"="{city}"]->.searchArea;

    // Sélection des lignes de métro et de leurs stations (membres)
    relation["route"="subway"](area.searchArea);
    out body;
    >;

    // Sélection des informations des stations de métro
    node["railway"="station"]["station"="subway"](area.searchArea);
    out body;
    """
    print (overpass_query)
    # Envoi de la requête à Overpass
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Dictionnaire pour stocker les lignes de métro avec les stations dans l'ordre
    line_stations_ordered = {}

    # Dictionnaire pour stocker les informations des stations (nom et position)
    station_info = {}

    # Traiter les données pour organiser les informations
    for element in data['elements']:
        if element['type'] == 'relation' and 'name' in element['tags']:
            # C'est une ligne de métro
            line_name = element['tags']['name']
            line_stations_ordered[line_name] = []
            
            # Parcours des membres de la relation pour collecter les stations dans l'ordre
            for member in element.get('members', []):
                if member['type'] == 'node':  # Vérifier que le membre est une station
                    station_id = member['ref']
                    line_stations_ordered[line_name].append(station_id)

        elif element['type'] == 'node' and 'name' in element['tags']:
            # C'est une station de métro, on enregistre les informations
            station_info[element['id']] = {
                "name": element['tags']['name'],
                "lat": element['lat'],
                "lon": element['lon']
            }

    # Affichage des lignes avec les stations dans l'ordre
    print("Lignes de métro avec stations dans l'ordre :")
    for line, station_ids in line_stations_ordered.items():
        print(f"Ligne {line} :")
        for station_id in station_ids:
            station = station_info.get(station_id, {})
            station_name = station.get("name", "Station inconnue")
            lat, lon = station.get("lat"), station.get("lon")
            if lat and lon:
                print(f"  - Station: {station_name} (Latitude: {lat}, Longitude: {lon})")
            else:
                print(f"  - Station: {station_name} (Position inconnue)")

def get_transport_data (city):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    
    [out:json][timeout:90];
    /* recherche des données avec .searcharea */ 
    area["name:fr"="{city}"]->.searcharea;
    (
      relation["type"="route"]["route"="subway"](area.searcharea);  
    );
    out ;
    >;
    out body qt ;
    """
    print(overpass_query)
    try:
        response = requests.post(overpass_url, data={'data': overpass_query})
    except Exception as e:
        print("Request error")
        print(e) 
        return {}
    
    if response.status_code == 200:
        # Parser la réponse JSON
        data = response.json()

    return data




""" 
[out:json][timeout:90];
    /* recherche des données avec .searcharea */ 
    
    (
      relation["water"]({{bbox}});  
      relation["building"]({{bbox}});  
      way["building"]({{bbox}});  
      relation["highway"]({{bbox}});  
      way["highway"]({{bbox}});  
      
    );
      
    /*added by auto repair*/
    (._;>;);
    /*end of auto repair*/
    out body ;
 """

""" marker 
<svg xmlns="http://www.w3.org/2000/svg" id="SvgjsSvg1077" x="0" y="0" version="1.1" viewBox="0 0 499.772 499.772" width="200" height="200" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs"><path d="M492.692 223.646 394.345 52.979a53.123 53.123 0 0 0-46.08-26.667H151.572a53.12 53.12 0 0 0-46.08 26.027L7.145 223.006a53.333 53.333 0 0 0 0 53.333l98.347 170.667a53.332 53.332 0 0 0 46.08 26.453h196.693a53.334 53.334 0 0 0 46.08-25.813l98.347-170.667a53.76 53.76 0 0 0 0-53.333z" fill="rgba(148, 6, 6, 1)"></path></svg>

<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" fill="none" viewBox="0 0 200 200" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs"><path fill="rgba(148, 6, 6, 1)" fill-rule="evenodd" d="M100 200c55.228 0 100-44.772 100-100S155.228 0 100 0 0 44.772 0 100s44.772 100 100 100Zm0-56.25c24.162 0 43.75-19.588 43.75-43.75S124.162 56.25 100 56.25 56.25 75.838 56.25 100s19.588 43.75 43.75 43.75Z" clip-rule="evenodd"></path></svg>
"""