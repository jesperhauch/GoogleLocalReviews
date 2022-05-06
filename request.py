
import requests
endpoint = "https://models.grace-dtu.2021.services/seldon/project-spaceembeddings/recommender-system/api/v0.1/predictions"

headers = {'Grace-Client-Secret': 'c0de6747-ffb6-4023-913f-53c8222435bb'}
IDs = ['101742583391038750118','100574642292837870712']
Ratings = [4,2]
payload = {"data": {"names": ["feature-1", "feature-2"],
                    "ndarray": [IDs, Ratings]}}
response = requests.post(endpoint, json = payload, headers = headers)

print(response.status_code)
print(response.text)
#print(response.json())