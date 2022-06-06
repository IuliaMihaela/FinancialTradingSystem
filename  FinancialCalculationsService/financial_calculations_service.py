from timeseries import *
from requests import put, get, post, delete
import json
from mpi4py import MPI

# root node
comm = MPI.COMM_WORLD


r = get('http://localhost:5000/users/login/api')
print(r.json())

users = r.json()
token = users["felicity"]["token"]
print("token:", token)

#  generating 100 random time series with 300 days
time_series = create_time_series(100, 300)

while True:
    # getting the messsage from the jobs queue
    r = get('http://localhost:7500/message_jobs/api', json={'username': 'felicity', 'token': token})
    try:
        job_response = json.loads(r.content.decode())
        job_assets = job_response["message_body"]["assets"]  # getting the assets from the response as a string
        list_assets = job_assets.split(',')  # convert job assets into a list

        if comm.rank == 0:
            tasks = [
                json.dumps({'parameter1': list_assets[0]}),
                json.dumps({'parameter1': list_assets[1]}),
                json.dumps({'parameter1': list_assets[2]}),
                json.dumps({'parameter1': list_assets[3]})
            ]
        else:
            tasks = None

        # Scatter parameters arrays
        unit = comm.scatter(tasks, root=0)

        p = json.loads(unit)
        print(f'[{comm.rank}]: parameters {p}')
        calc = predict_value(linear_fit(time_series[p['parameter1']]), 301)

        # gather results
        result = comm.gather(calc, root=0)
        if comm.rank == 0:
            print("[root]: Result is ", result)

        avg_result = sum(result) / len(result)
        print(f"Avg Result is: {avg_result}")

        print("pushing a result into the queue")
        job_id = job_response["message_body"]["id"]
        r = post('http://localhost:7500/message_results/api', json={'job_id': job_id,'username': 'felicity', "token": token, "timestamp": "15-04-2022 15:54", "assets": avg_result})
        print(r.content.decode())
        job_response = json.loads(r.content.decode())
        print(job_response)

    except:
        break



########################################  testing with input list of assets
# comm = MPI.COMM_WORLD
# time_series = create_time_series(100, 300)
#
# list_assets = [10, 17, 23, 56, 60]
#
# if comm.rank == 0:
#     tasks = [
#         json.dumps({'parameter1': list_assets[0]}),
#         json.dumps({'parameter1': list_assets[1]}),
#         json.dumps({'parameter1': list_assets[2]}),
#         json.dumps({'parameter1': list_assets[3]}),
#         json.dumps({'parameter1': list_assets[4]})
#     ]
#
# else:
#     tasks = None
#
# unit = comm.scatter(tasks, root=0)
# p = json.loads(unit)
# print(f'[{comm.rank}]: parameters {p}')
# calc = predict_value(linear_fit(time_series[p['parameter1']]), 301)
# # gather results
# result = comm.gather(calc, root=0)
# if comm.rank == 0:
#     print("[root]: Result is ", result)
#     avg_result = sum(result) / len(result)
#     print(f"Avg Result is: {avg_result}")
#








