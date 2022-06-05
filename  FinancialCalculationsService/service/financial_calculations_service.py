import queue
from MasterDataService.service.master_data_service import *
from AuthenticationService.service.authentication_service import *
from MessageQueuesService.service.models import Jobs_Queue, Results_Queue
from MessageQueuesService.service import api, db
from MessageQueuesService.configfile import config
from timeseries import *
from requests import put, get, post, delete
import json

def calculate_result(list_assets):
    list_time_series = create_time_series(len(list_assets), 10)
    predicted_values = []
    for i in range(len(list_time_series)):
        model = linear_fit(list_time_series[i])
        predicted_value = predict_value(model, list_assets[i])
        predicted_values.append(predicted_value)
    result = sum(predicted_value) / len(predicted_values)
    return result

class Calculations(Resource):
    def get(self):
        data = request.json
        str_assets = data['assets']  # '1,2,3'
        list_assets = str_assets.split(',')
        result = calculate_result(list_assets)



###################################################################################

r = get('http://localhost:5000/users/login/api')
print(r.json())

users = r.json()
token = users["felicity"]["token"]
print("token:", token)

r = get('http://localhost:5000/users/login/api')
print(r.json())

users = r.json()
token = users["felicity"]["token"]
print("token:", token)
time_series = create_time_series(100, 300)
while True:
    r = get('http://localhost:7500/message_jobs/api', json={'username': '', 'token': token})
    job_response = json.loads(r.content.decode())
    job_assets = job_response["message_body"]["assets"]
    list_assets = job_assets.split(',')
    for asset in list_assets:
        ts = time_series[asset]
        model = linear_fit(ts)
        pred = predict_value(model,301)








