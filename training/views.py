from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from stream.models import Process, ConsolidatedMSE
from .mqtt_logic import *
import random, string
from django.views.decorators.csrf import csrf_exempt

NUMBER_OF_NODES = 6
PROCESS_ID = "12"

def generate_pid(length, characters=string.ascii_letters + string.digits):
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def train(request):
    global NUMBER_OF_NODES
    global PROCESS_ID
    #before training abort and clean the topic
    if request.method == "POST":
        post_data = request.body
        body = json.loads(post_data)
        mu = float(body["stepSize"])
        iterations = int(body["iterations"])
        weight_size = int(body["weightSize"])
        error_prob = float(body["error_prob"])
        strategy = body["strategy"]
        algo = body["algo"]
        alpha = body["alpha"]
        beta = body["beta"]
        p_id = generate_pid(10)
        process = Process(p_id=p_id, strategy=strategy, error_prob=error_prob, algo=algo, alpha = alpha, beta = beta) #creating a new process
        PROCESS_ID = p_id
        process.save()
        number_nodes = int(body["nodeNumber"])
        NUMBER_OF_NODES = number_nodes
        # return JsonResponse(iterations, safe=False)
        for _iter in range(number_nodes):
            clear_retained_messages(_iter) #all topics cleared
        for _iter in range(number_nodes):
            # neighbours, edge_weights = generate_ne_we_data(_iter, [[1]], 1)
            if strategy == "INCREMENTAL":
                neighbours, edge_weights = generate_ne_we_data_inc(_iter)
            else:
                neighbours, edge_weights = generate_ne_we_data(_iter)
            publish_ne_we_data(_iter, strategy, neighbours, edge_weights, p_id, mu, iterations, weight_size, error_prob, algo, alpha, beta)
        
    return JsonResponse("OK! Training Started!", safe=False)

@csrf_exempt
def abort(request):
    for _iter in range(NUMBER_OF_NODES):
        sync_node(_iter)
    return JsonResponse("Training Aborted!", safe=False)

@csrf_exempt
def get_last_train_data(request):
    process = Process.objects.filter()
    process_id = process.last().p_id
    strategy = process.last().strategy
    process_object = {
        "p_id": process_id,
        "strategy": strategy
    }
    return JsonResponse(process_object, safe=False)

@csrf_exempt
def get_process_data(request,p_id):
    if p_id == "0":
        process = Process.objects.filter().last()
    else:
        process = Process.objects.filter(p_id=p_id)
        if process.exists() == False:
            return JsonResponse("Process Doesn't exist!", safe=False)
    cmse_query = ConsolidatedMSE.objects.filter(process=process)
    if cmse_query.exists() == False:
        return JsonResponse("Training hasn't started yet!", safe=False)
    return_payload = []
    for cmse in cmse_query:
        cmse_object = {
            "strategy": cmse.process.strategy,
            "device": cmse.device.device_id,
            "p_id": cmse.process.p_id,
            "mse_array": cmse.mse_array
        }
        return_payload.append(cmse_object)
    return JsonResponse(return_payload, safe=False)