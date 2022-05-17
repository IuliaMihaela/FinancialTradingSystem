from requests import put, get, post, delete
import json

r = get('http://localhost:5000/users/login/api')
print(r.json())

users = r.json()
token = users["felicity"]["token"]
print("token:", token)


# print("create jobs queue")
# r = post('http://localhost:7500/jobs_queue/api', json={'username': 'felicity', 'token': token})
# print(r.content.decode())
# response = json.loads(r.content.decode())
# print(response)
#
#
# print("create results queue")
# r = post('http://localhost:7500/results_queue/api', json={'username': 'felicity', 'token': token})
# print(r.content.decode())
# response = json.loads(r.content.decode())
# print(response)
#
#
#
#
# print("pushing a job into the queue")
# job_id = ""
# r = post('http://localhost:7500/message_jobs/api', json={'job_id': job_id,'username': '', "timestamp": "15-04-2022 15:54", "status": "done", "date_range": "13-15", "assets": "1,2,3,4,5,11"})
# print(r.content.decode())
# job_response = json.loads(r.content.decode())
# print(job_response)
#
#
# print("pulling a job")
# r = get('http://localhost:7500/message_jobs/api', json={'username': '', 'token': token})
# print(r.content.decode())
# job_response = json.loads(r.content.decode())
# print(job_response)
#
#
#
# print("pushing a result into the queue")
# job_id = ""
# r = post('http://localhost:7500/message_results/api', json={'job_id': job_id,'username': '', "token": token, "timestamp": "15-04-2022 15:54", "assets": "1,2,3,4,5,11"})
# print(r.content.decode())
# job_response = json.loads(r.content.decode())
# print(job_response)
#
#
# print("pulling a result")
# r = get('http://localhost:7500/message_results/api')
# print(r.content.decode())
# job_response = json.loads(r.content.decode())
# print(job_response)





















