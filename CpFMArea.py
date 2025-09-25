from arcgis.gis import GIS
from arcgis.map import OfflineMapAreaManager
import time
from typing import Optional
import requests
import arcgis
import json
print(arcgis.__version__)
from arcgis import env
env.verbose = True

# import warnings
# warnings.filterwarnings("ignore")


 

# === CONFIGURATION ===
CREATE_URL = "https://gis.israntique.org.il/arcgis/rest/services/Utilities/OfflinePackaging/GPServer/SetupMapArea/submitJob"
GIS_REFERER_URL = "https://gis.israntique.org.il/portal"
GIS_TOKEN_URL = "https://gis.israntique.org.il/portal/sharing/rest/generateToken"
GIS_USERNAME = ""
GIS_PASSWORD = ""

def get_token() -> Optional[str]:
    """Function to get GIS token."""
    url = GIS_TOKEN_URL
 
    payload = {
        'username': GIS_USERNAME,
        'password': GIS_PASSWORD,
        'client': 'requestip',
        'expiration': '24',
        'f': 'json',
        'referer': GIS_REFERER_URL
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.post(url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)
        return response.json().get('token')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None  
    

def create_offline_map_area(title, snippet, description, properties, text, target_id, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{GIS_USERNAME}/addItem"
 
    payload = {
        'title': str(title),
        'snippet': str(snippet),
        'description': str(description),
        'thumbnailurl': f'https://gis.israntique.org.il/portal/sharing/rest/content/items/{target_id}/info/thumbnail/ago_downloaded.png?f=json&token={token}',
        'type': 'Map Area',
        'properties': str(properties),
        'text': str(json.dumps(text)),
        'f': 'json',
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.post(url, headers=headers, data=payload, files=files, verify=False)
        # print(response.text)

        url2 = GIS_REFERER_URL + f"/sharing/rest/content/users/{GIS_USERNAME}/items/{target_id}/update"

        response2 = requests.post(url2, headers=headers, data={"id": target_id, "token": token}, files=files, verify=False)
        # print(response2.text)

        return response.json().get('id')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None  
    

def add_relationship(itemid, targetid, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{GIS_USERNAME}/addRelationship"
 
    payload = {
        'f': 'json',
        'relationshipType': 'Map2Area',
        'destinationItemID': itemid,
        'originItemID': targetid,
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.post(url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)

        return response.json()
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None 

def get_resource(resource_endpoint, itemid, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = f"https://gis.israntique.org.il/portal/sharing/rest/content/users/{GIS_USERNAME}/items/{itemid}/resources/{resource_endpoint}"
    
 
    payload = {
        'f': 'json',
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.get(url, headers=headers, params=payload, files=files, verify=False)
        print(response.text)

        return response.json()
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None

def add_resource(resource_endpoint, text, itemid, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{GIS_USERNAME}/items/{itemid}/addResources"
 
    payload = {
        'f': 'json',
        'filename': resource_endpoint[6:],
        'resourcesPrefix': 'areas',
        'text': str(json.dumps(text)),
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.post(url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)

        return response.json().get('itemId')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None

def create_shared_resource(itemid, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{GIS_USERNAME}/items/{itemid}/share"
 
    payload = {
        'everyone': 'false',
        'org': 'true',
        'groups': '',
        'f': 'json',
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.post(url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)
        return response.json()
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None

def create_by_item_id(mapAreaItemID: str, token) -> Optional[str]:
    """Function to create an offline map area."""
    url = CREATE_URL
 
    payload = {
        "mapAreaItemID": mapAreaItemID,
        'tileServices': '[{"url":"https://gis.israntique.org.il/arcgis/rest/services/MapCacheNational_2019/MapServer","levels":"0,1,2,3,4,5,6"}]',
        'f': 'json',
        'token': token,
    }
 
    headers = {}
    files = []
 
    try:
        response = requests.get(url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)
        return response.json().get('id')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None  

token = get_token()

SOURCE_ITEM_ID = ""
TARGET_ITEM_ID = ""

# === LOGIN ===
gis = GIS(url=GIS_REFERER_URL, token=token, verify_cert=False)

# Get the source offline map and its offline areas
source_map_area_manager_item = gis.content.get(SOURCE_ITEM_ID)
offline_areas  = OfflineMapAreaManager(source_map_area_manager_item, gis=gis).list()

for ids in offline_areas:
   print('found id in source map: ' + ids.title)

# Get the target offline map and its offline areas
offline_map_item = gis.content.get(TARGET_ITEM_ID)
offline_map = OfflineMapAreaManager(offline_map_item, gis=gis)
offline_map._token = token

for ids in offline_map.list():
   print('found id in target_map: ' + ids.title)
   
for offline_area in offline_areas:

    print('Creating offline map area for ' + offline_area.title)

    try:    
        #trying to get map area geometry data:
        polygon=False
        if 'area' in offline_area.properties: #this means its polygon
            polygon=True
            area_data = gis.content.get(offline_area.properties['area']['itemId']).get_data()
        else: #this means its extent
            area_data = offline_area.properties['extent']
        
        print("Created offline map area with item ID:", offline_area.id)
        itemid = create_offline_map_area(title=offline_area.title, snippet=offline_area.snippet, description=offline_area.description, properties=offline_area.properties, text=area_data, target_id=TARGET_ITEM_ID, token=token)
        shared_req = create_shared_resource(itemid=itemid, token=token)
        relationship = add_relationship(itemid=itemid, targetid=TARGET_ITEM_ID, token=token)
        if polygon:
            geometry = get_resource(resource_endpoint=offline_area.properties['area']['resource'], itemid=offline_area.properties['area']['itemId'], token=token)
            print(geometry)
            itemidresource = add_resource(resource_endpoint=offline_area.properties['area']['resource'], text=geometry, itemid=itemid, token=token)
            create_by_item_id(itemidresource, token=token)

    except Exception as e:
        print('Failed creating map area for ' + offline_area.title)
        print("Error details:", e)

print("\n=== END OF COPY OPERATION ===")