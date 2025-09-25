from arcgis.gis import GIS
from arcgis.map import OfflineMapAreaManager
import time
from typing import Optional
import requests
import arcgis
import json
import sys
import os
from config import USERNAME, PASSWORD, SOURCE, TARGET
print(arcgis.__version__)
from arcgis import env
env.verbose = True

# import warnings
# warnings.filterwarnings("ignore")


 

# === CONFIGURATION ===
CREATE_URL = "https://gis.israntique.org.il/arcgis/rest/services/Utilities/OfflinePackaging/GPServer/SetupMapArea/submitJob"
GIS_REFERER_URL = "https://gis.israntique.org.il/portal"
GIS_TOKEN_URL = "https://gis.israntique.org.il/portal/sharing/rest/generateToken"
# Credentials will be passed as command line arguments

def get_token(username: str, password: str) -> Optional[str]:
    """Function to get GIS token."""
    url = GIS_TOKEN_URL
 
    payload = {
        'username': username,
        'password': password,
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
    
def create_offline_map_area(title, snippet, description, properties, text, target_id, token, username: str) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{username}/addItem"
 
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

        url2 = GIS_REFERER_URL + f"/sharing/rest/content/users/{username}/items/{target_id}/update"

        response2 = requests.post(url2, headers=headers, data={"id": target_id, "token": token}, files=files, verify=False)
        # print(response2.text)

        return response.json().get('id')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None  
    
def add_relationship(itemid, targetid, token, username: str) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{username}/addRelationship"
 
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

def get_resource(resource_endpoint, itemid, token, username: str) -> Optional[str]:
    """Function to create an offline map area."""
    url = f"https://gis.israntique.org.il/portal/sharing/rest/content/users/{username}/items/{itemid}/resources/{resource_endpoint}"
    
 
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

def add_resource(resource_endpoint, text, itemid, token, username: str) -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{username}/items/{itemid}/addResources"
 
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

def create_shared_resource(sharing_data, groups, itemid:str='', token:str='', username: str='') -> Optional[str]:
    """Function to create an offline map area."""
    url = GIS_REFERER_URL + f"/sharing/rest/content/users/{username}/items/{itemid}/share"
 
    payload = {
        'everyone': str(sharing_data=='everyone').lower(),
        'org': str(sharing_data=='org').lower(),
        'groups': groups,
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

def main(source_area_map_id: str, target_area_map_id: str, owner_username: str, owner_password: str):
    """Main function to execute the offline map area copying process."""
    token = get_token(owner_username, owner_password)
    
    if not token:
        print("Failed to get authentication token. Exiting.")
        return

    # === LOGIN ===
    gis = GIS(url=GIS_REFERER_URL, token=token, verify_cert=False)

    # Get the source offline map and its offline areas
    source_map_area_manager_item = gis.content.get(source_area_map_id)
    offline_areas = OfflineMapAreaManager(source_map_area_manager_item, gis=gis).list()

    for ids in offline_areas:
        print('found id in source map: ' + ids.title)

    # Get the target offline map and its offline areas
    offline_map_item = gis.content.get(target_area_map_id)
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
            itemid = create_offline_map_area(title=offline_area.title, snippet=offline_area.snippet, description=offline_area.description, properties=offline_area.properties, text=area_data, target_id=target_area_map_id, token=token, username=owner_username)
            groups = ",".join([g.id for g in offline_map_item.sharing.shared_with.get("groups", [])])
            access_data = offline_map_item.access
            shared_req = create_shared_resource(access_data,groups, itemid=itemid, token=token, username=owner_username)
            relationship = add_relationship(itemid=itemid, targetid=target_area_map_id, token=token, username=owner_username)
            if polygon:
                geometry = get_resource(resource_endpoint=offline_area.properties['area']['resource'], itemid=offline_area.properties['area']['itemId'], token=token, username=owner_username)
                print(geometry)
                itemidresource = add_resource(resource_endpoint=offline_area.properties['area']['resource'], text=geometry, itemid=itemid, token=token, username=owner_username)
                create_by_item_id(itemidresource, token=token)

        except Exception as e:
            print('Failed creating map area for ' + offline_area.title)
            print("Error details:", e)

    print("\n=== END OF COPY OPERATION ===")

if __name__ == "__main__":
    # Load configuration from environment variables
    source_area_map_id = SOURCE
    target_area_map_id = TARGET
    owner_username = USERNAME
    owner_password = PASSWORD
    
    # Check if all required environment variables are set
    if not all([source_area_map_id, target_area_map_id, owner_username, owner_password]):
        print("Error: Missing required environment variables.")
        print("Please ensure the following variables are set in config.env:")
        print("- SOURCE: Source area map ID")
        print("- TARGET: Target area map ID") 
        print("- USERNAME: GIS portal username")
        print("- PASSWORD: GIS portal password")
        print("\nYou can copy config.env.example to config.env and fill in your values.")
        sys.exit(1)
    
    main(source_area_map_id, target_area_map_id, owner_username, owner_password)

