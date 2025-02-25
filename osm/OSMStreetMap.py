
import requests

def osm_get_indirect_node (streetmap_data, node_id):
    """
    Retrieve an indirect node from the street information dictionary.

    Args:
        transport_info (dict): A dictionary containing osm street information, including nodes.
        node_id (int): The ID of the node to retrieve.

    Returns:
        dict: The node information corresponding to the given node ID.
    """
    return streetmap_data['nodes'][node_id]

def overpass_request(latitude, longitude, radius):
    """
    Overpass request from location and radius data 
    """
    # overpass URL 
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Requête Overpass
    query = f"""
    [out:json];
    (
    way["highway"~"^(trunk|primary|secondary|tertiary|unclassified|residential)$"](around:{radius}, {latitude}, {longitude});
    way["building"](around:{radius}, {latitude}, {longitude});
      
    );
    (._;>;);
    
    out body;
    >;
    
    
    """

    print("overpass request : ")
    print(query) 
    print("")
    
    # Récupération des données via Overpass API
    response = requests.get(overpass_url, params={"data": query})

    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête : {response.status_code}")

    data = response.json()
    
    return data 

def osm_extraction (streetmap_data):

    street_info = {"relations":{},"ways":{}, "nodes":{}} 
   
    if 'elements' not in streetmap_data:
        print("Aucune donnée récupérée pour la ville ")
        return street_info
    else:
        for element in streetmap_data['elements']:
            #print (element['type'])
            if element['type'] == 'relation':
                street_info['relations'][element['id']] = element
            elif element['type'] == 'way':
                street_info['ways'][element['id']] = element
            elif element['type'] == 'node':
                street_info['nodes'][element['id']] = element
    
    return street_info

def osm_extract_data (streetmap_data):
    streetmap_2d_data = {"street":[],"building":[], "unclassified":[]}
    ways = []

    for way in streetmap_data['ways'].values():
        ways_node = []
        if 'tags' in way:
            if 'highway' in way['tags']:
                #build a street
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                            #if "tags" in node:
                            #    print (node['tags'])
                            anoted_node = {
                                "lat": node["lat"],
                                "lon": node["lon"],
                                "id": node["id"],
                                "way_id": way["id"],
                                
                            }
                            ways_node.append (anoted_node)
                        
                    street = {
                        "id": way['id'],
                        "highway": way['tags']['highway'],
                        "nodes":ways_node
                    }
                    streetmap_2d_data["street"].append (street)

            elif 'building' in way['tags']:
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                            if "tags" not in node:
                                
                                anoted_node = {
                                    "lat": node["lat"],
                                    "lon": node["lon"],
                                    "id": node["id"],
                                    "way_id": way["id"],
                                    
                                }
                                ways_node.append (anoted_node)
                        
                    building = {
                        "id": way['id'],
                        "building": way['tags']['building'],
                        "nodes":ways_node
                    }
                    streetmap_2d_data["building"].append (building)

            else:
                if 'nodes' in way:
                    for nodeid in way["nodes"]:
                        node = osm_get_indirect_node (streetmap_data, nodeid)
                        # Check if the node has lat and lon
                        
                        if "lat" in node and "lon" in node:
                            if "tags" not in node:
                                
                                anoted_node = {
                                    "lat": node["lat"],
                                    "lon": node["lon"],
                                    "id": node["id"],
                                    "way_id": way["id"],
                                    
                                }
                                ways_node.append (anoted_node)
                        
                    unclassified = {
                        "id": way['id'],
                        "building": way['tags']['building'],
                        "nodes":ways_node
                    }
                    streetmap_2d_data["unclassified"].append (unclassified)

    return streetmap_2d_data