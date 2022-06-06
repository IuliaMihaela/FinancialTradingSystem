# import queue
# from MasterDataService.service.master_data_service import *
# from AuthenticationService.service.authentication_service import *
# from MessageQueuesService.service.models import Jobs_Queue, Results_Queue
# from MessageQueuesService.service import api, db
# from MessageQueuesService.configfile import config
from timeseries import *
from requests import put, get, post, delete
import json
from mpi4py import MPI

# def calculate_result(list_assets):
#     list_time_series = create_time_series(len(list_assets), 10)
#     predicted_values = []
#     for i in range(len(list_time_series)):
#         model = linear_fit(list_time_series[i])
#         predicted_value = predict_value(model, list_assets[i])
#         predicted_values.append(predicted_value)
#     result = sum(predicted_values) / len(predicted_values)
#     return result
#
# class Calculations(Resource):
#     def get(self):
#         data = request.json
#         str_assets = data['assets']  # '1,2,3'
#         list_assets = str_assets.split(',')
#         result = calculate_result(list_assets)
#


###################################################################################
# comm = MPI.COMM_WORLD
#
#
# r = get('http://localhost:5000/users/login/api')
# print(r.json())
#
# users = r.json()
# token = users["felicity"]["token"]
# print("token:", token)
#
# #  generating 100 random time series with 300 days
# time_series = create_time_series(100, 300)
#
# while True:
#     # getting the messsage from the jobs queue
#     r = get('http://localhost:7500/message_jobs/api', json={'username': 'felicity', 'token': token})
#     # job_assets = input(": ")
#     try:
#         job_response = json.loads(r.content.decode())
#         job_assets = job_response["message_body"]["assets"]  # getting the assets from the response as a string
#         list_assets = job_assets.split(',')  # convert to assets into a list
#
#         if comm.rank == 0:
#             tasks = [
#                 json.dumps({'parameter1': list_assets[0]}),
#                 json.dumps({'parameter1': list_assets[1]}),
#                 json.dumps({'parameter1': list_assets[2]}),
#                 json.dumps({'parameter1': list_assets[3]})
#             ]
#         else:
#             tasks = None
#
#         unit = comm.scatter(tasks, root=0)
#         p = json.loads(unit)
#         print(f'[{comm.rank}]: parameters {p}')
#         calc = predict_value(linear_fit(time_series[p['parameter1']]), 301)
#         # gather results
#         result = comm.gather(calc, root=0)
#         if comm.rank == 0:
#             print("[root]: Result is ", result)
#
#         avg_result = sum(result) / len(result)
#         print(f"Avg Result is: {avg_result}")
#
#         print("pushing a result into the queue")
#         job_id = job_response["message_body"]["id"]
#         r = post('http://localhost:7500/message_results/api', json={'job_id': job_id,'username': 'felicity', "token": token, "timestamp": "15-04-2022 15:54", "assets": avg_result})
#         print(r.content.decode())
#         job_response = json.loads(r.content.decode())
#         print(job_response)
#
#     except:
#         break
#


########################################  testing 1
# comm = MPI.COMM_WORLD
# time_series = create_time_series(100, 300)
# scatter_tasks = None
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
#     scatter_tasks = [None] * comm.size
#     current_proc = 0
#     for task in tasks:
#         if scatter_tasks[current_proc] is None:
#             scatter_tasks[current_proc] = []
#         scatter_tasks[current_proc].append(task)
#         current_proc = (current_proc + 1) % comm.size
#
# else:
#     tasks = None
#
# units = comm.scatter(tasks, root=0)
# calcs = []
#
# if units is not None:
#     for unit in units:
#         p = json.loads(unit)
#         print(f'[{comm.rank}]: parameters {p}')
#
#         calc = predict_value(linear_fit(time_series[p['parameter1']]), 301)
#
#         calc = [calc, comm.rank]
#         calcs.append(calc)
#
#
# # gather results
# result = comm.gather(calcs, root=0)
#
# if comm.rank == 0:
#     print("[root]: Result is ", result)
#     avg_result = sum(result) / len(result)
#     print(f"Avg Result is: {avg_result}")
#
#



########################################  testing 2
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
#







