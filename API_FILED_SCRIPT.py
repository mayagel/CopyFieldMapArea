from arcgis.gis import GIS
from arcgis.map import OfflineMapAreaManager
import time
from typing import Optional
import requests
from config import USERNAME, PASSWORD, SOURCE, TARGET

# === CONFIGURATION ===
GIS_REFERER_URL = "https://gis.israntique.org.il/portal"
GIS_TOKEN_URL = "https://gis.israntique.org.il/portal/sharing/rest/generateToken"


def get_token() -> Optional[str]:
    """Function to get GIS token."""
    url = GIS_TOKEN_URL
 
    payload = {
        'username': USERNAME,
        'password': PASSWORD,
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

token = get_token()

# === LOGIN ===
try:
    gis = GIS(url=GIS_REFERER_URL, username=USERNAME, password=PASSWORD)
except:
    gis = GIS(url=GIS_REFERER_URL, token=token)

# Get the source offline map and its offline areas
source_map_area_manager_item = gis.content.get(SOURCE)
offline_areas  = OfflineMapAreaManager(source_map_area_manager_item, gis=gis).list()

for ids in offline_areas:
   print('found id in source map: ' + ids.title)

# Get the target offline map and its offline areas
offline_map_item = gis.content.get(TARGET)
offline_map = OfflineMapAreaManager(offline_map_item, gis=gis)
offline_map._token = token

for ids in offline_map.list():
   print('found id in target_map: ' + ids.title) # this works as expected ad prints all the offline map area names

#some min and max scale just for the example
#Min scale for map areas - World scale
map_area_min_scale = 147914382
#Max scale for map areas - Neighborhood scale
map_area_max_scale = 20000

   
for offline_area in offline_areas:
    print('Creating offline map area for ' + offline_area.title)
    try:     
        map_area = offline_map.create(area=source_map_area_manager_item.extent,
                                                    item_properties=offline_area.properties,
                                                    refresh_schedule='daily',
                                                    min_scale=map_area_min_scale,
                                                    max_scale=map_area_max_scale)

    except Exception as e:
        print('Failed creating map area for ' + offline_area.title)
        print("Error details:", e)

print("\n=== END OF COPY OPERATION ===")