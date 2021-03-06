import queue
from MasterDataService.service.master_data_service import *
from AuthenticationService.service.authentication_service import *
from MessageQueuesService.service.models import Jobs_Queue, Results_Queue
from MessageQueuesService.service import api, db
from MessageQueuesService.configfile import config

# queue_jobs = queue.Queue
# queue_results = queue.Queue

LENGTH_QUEUE = config["QUEUE"]["queue_limit"]

def create_response_worker_queue(message):
    # creating the response that is sent from the worker to the message queue
    return {
        "source": "worker",
        "destination": "http://127.0.0.1:7500",
        "message_body": message
    }

def create_response_queue_worker(message):
    # creating the response that is sent rom the message queue to the worker
    return {
        "source": "http://127.0.0.1:7500",
        "destination": "worker",
        "message_body": message
    }

def create_response_masterdata_queue(message):
    # creating the response that is sent to from the master data service to the message queue service
    return {
        "source": "http://127.0.0.1:5001",
        "destination": "http://127.0.0.1:7500",
        "message_body": message
    }

def create_response_queue_masterdata(message):
    # creating the response that is sent from the message queue service to the master data service
    return {
        "source": "http://127.0.0.1:7500",
        "destination": "http://127.0.0.1:5001",
        "message_body": message
    }

def validate_user_permission_queue(username, token):
    token_state = verify_token(username, token)
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is a secretary or manager
    if username not in users.keys() or token.split('-')[0] != "administrator":
        return {"error": "Authorization Error"}
    return ""

def validate_user_permission_push_pull(username, token):
    token_state = verify_token(username, token)
    # checking if the token is valid
    if token_state['success'] == False:
        return {"error": "Token not valid"}
    # checking if the user is not authorized, meaning that is not logged in or is a secretary
    if username not in users.keys() or token.split('-')[0] == "secretary":
        return {"error": "Authorization Error"}
    return ""

def validate_push_job(data):
    # checking if all data needed for pushing a job was provided
    if "job_id" not in data:
        return {"error": "job_id not provided"}
    if "username" not in data:
        return {"error": "no user provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "status" not in data:
        return {"error": "no status provided"}
    if "date_range" not in data:
        return {"error": "date_range not provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""


def validate_pull_job(data):
    # checking if all data needed for pulling a job was provided
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "token not provided"}
    return ""

def validate_queue(data):
    # checking if all data needed for when creating, deleting or listing a queue is provided
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "token not provided"}
    return ""


def validate_push_result(data):
    # checking if all data needed for pushing a result was provided
    if "job_id" not in data:
        return {"error": "job_id not provided"}
    if "username" not in data:
        return {"error": "no user provided"}
    if "token" not in data:
        return {"error": "token not provided"}
    if "timestamp" not in data:
        return {"error": "no timestamp provided"}
    if "assets" not in data:
        return {"error": "assets not provided"}
    return ""


def pull_job():
    if queue_jobs.empty():
        return {"error": "Sorry, but the queue you wanted to pull the message out of is empty, so please try again later"}
    job = queue_jobs.get()  # pull the job from the queue
    delete_message_job_db(job)  # delete the job from the database
    return job.serialize()

def push_job(job):
    if queue_jobs.qsize() >= LENGTH_QUEUE:
        return {"error": "Sorry, but the queue you wanted to push the message in is full, so please try again later"}
    queue_jobs.put(job)  # push the job into the queue
    return ""


def pull_result():
    if queue_results.empty():
        return {"error": "Sorry, but the queue you wanted to pull the message out of is empty, so please try again later"}
    result = queue_results.get()  # pull the result from the queue
    delete_message_result_db(result)  # delete the result from the database
    return result.serialize()

def push_result(result):
    if queue_results._qsize() > LENGTH_QUEUE:
        return {"error": "Sorry, but the queue you wanted to push the message in is full, so please try again later"}
    queue_results.put(result)  # push the result into the queue
    return ""


def create_message_job_db(data):  # creating and adding the job description from the queue in the database
    # creating an instance of class Job_Queue
    new_job = Jobs_Queue(id=data["job_id"], username=data['username'], timestamp=data['timestamp'], status=data['status'], date_range=data['date_range'], assets=data['assets'])
    db.session.add(new_job)  # add job to database
    db.session.commit()  # save changes to database
    return new_job.serialize()

def create_message_result_db(data): # creating and adding the result of a job from the queue in the database
    # creating an instance of class Result_Queue
    new_result = Results_Queue(job_id=data['job_id'], timestamp=data['timestamp'], assets=data['assets'])
    db.session.add(new_result)  # add result to database
    db.session.commit()  # save changes to database
    return new_result.serialize()

def delete_message_job_db(job):
    try:
        # get job by the job id
        job = Jobs_Queue.query.get(job["job_id"])

        db.session.delete(job)  # delete the job
        db.session.commit()  # save changes
        return {"success": True}
    except:
        return "Job not found"


def delete_message_result_db(result):
    try:
        # get result by the job id
        result = Results_Queue.query.get(result["job_id"])

        db.session.delete(result)  # delete the result
        db.session.commit()  # save changes
        return {"success": True}
    except:
        return "Result not found"


class Message_Jobs(Resource):  # for pushing and pulling jobs into and out of the jobs queue
    def post(self):  # for pushing a job into the queue
        validation = validate_push_job(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json

        # user permission is already checked in the master data service when requesting a job

        job = fetch_job(data["job_id"])
        response = push_job(job)
        if not response:  # if the jobs queue is not full
            create_message_job_db(data)  # store it in the databse

        response = create_response_masterdata_queue(response)
        return response

    def get(self):  # for pulling a job out of the queue
        job = pull_job()
        response = create_response_queue_worker(job)
        return response



class Message_Results(Resource):  # for pushing and pulling results into and out of the results queue
    def post(self):  # for pushing a result into the queue
        validation = validate_push_result(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_push_pull(data["username"],
                                                          data["token"])  # check if the user has permission
        if validation != "":
            return validation

        result = fetch_result(data["job_id"])
        response = push_result(result)
        if not response:  # if the results queue is not full
            create_message_result_db(data)
        response = create_response_worker_queue(result)
        return response

    def get(self):  # for pulling a result out of the queue
        result = queue_results.get()
        response = create_response_queue_masterdata(result)
        return response


def delete_jobs_queue():
    try:
        del queue_jobs
        # delete jobs from the queue in the database
        db.session.query(Jobs_Queue).delete()
        db.session.commit()
        return {"success": True}
    except:
        return {"error": "The queue for the jobs does not exist"}


def delete_results_queue():
    try:
        del queue_results
        # delete results from the queue in the database
        db.session.query(Results_Queue).delete()
        db.session.commit()
        return {"success": True}
    except:
        return {"error": "The queue for the results does not exist"}



class Jobs_Queue(Resource):  # for creating, deleting and listing job queue
    def post(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                          data["token"])  # check if the user has permission
        if validation != "":
            return validation
        global queue_jobs
        queue_jobs = queue.Queue
        return {"success": True}


    def get(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                    data["token"])  # check if the user has permission
        if validation != "":
            return validation

        response = create_response_queue_worker(queue_jobs)
        return response



    def delete(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                    data["token"])  # check if the user has permission
        if validation != "":
            return validation

        result = delete_jobs_queue()
        response = create_response_queue_worker(result)
        return response


class Results_Queue(Resource):  # for creating, deleting and listing results queue
    def post(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                          data["token"])  # check if the user has permission
        if validation != "":
            return validation
        global queue_results
        queue_results = queue.Queue
        return {"success":True}

    def get(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                    data["token"])  # check if the user has permission
        if validation != "":
            return validation

        response = create_response_queue_worker(queue_results)
        return response

    def delete(self):
        validation = validate_queue(request.json)  # check if all data was provided
        if validation != "":
            return validation
        data = request.json
        validation = validate_user_permission_queue(data["username"],
                                                    data["token"])  # check if the user has permission
        if validation != "":
            return validation

        result = delete_results_queue()
        response = create_response_queue_worker(result)
        return response


api.add_resource(Message_Jobs, '/message_jobs/api')
api.add_resource(Message_Results, '/message_results/api')
api.add_resource(Jobs_Queue, '/jobs_queue/api')
api.add_resource(Results_Queue, '/results_queue/api')

























