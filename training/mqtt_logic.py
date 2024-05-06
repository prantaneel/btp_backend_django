from .mqtt_client import MQTTClient
import json

network_graph = [
    [0.5, 0.25, 0.25, 0],
    [0.25, 0.5, 0.25, 0],
    [0, 0.25, 0.5, 0.25],
    [0, 0.25, 0.25, 0.5]
]
Number_of_nodes = 4
network_graph_incremental = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0]
]

def network_fail_testing(failed_nodes = [], graph=network_graph):
    new_network_graph = graph
    N_size = len(graph)
    for index in failed_nodes:
        for _iter in range(N_size):
            new_network_graph[index][_iter] = 0
            new_network_graph[_iter][index] = 0
    return new_network_graph

def generate_ne_we_data_inc(index, graph = network_graph_incremental, N = Number_of_nodes, threshold = 0):
    neighbours = []
    edge_weights = []
    for _iter in range(N):
        if graph[index][_iter] > threshold:
            neighbours.append(_iter)
            edge_weights.append(graph[index][_iter])
    return neighbours, edge_weights

def generate_ne_we_data(index, graph=network_graph, N=Number_of_nodes, threshold = 0):
    graph = network_fail_testing(failed_nodes=[], graph=graph)
    neighbours = []
    edge_weights = []
    weight_sum = 0
    for _iter in range(N):
        if _iter==index:
            continue
        if graph[index][_iter] > threshold:
            neighbours.append(_iter)
            weight_sum = weight_sum + graph[index][_iter]
            edge_weights.append(graph[index][_iter])
    weight_sum = weight_sum + graph[index][index]
    weight_sum = 1 if weight_sum == 0 else weight_sum
    edge_weights.append(graph[index][index])
    for _it in range(len(edge_weights)):
        edge_weights[_it] = edge_weights[_it] / weight_sum
    return neighbours, edge_weights

def publish_ne_we_data(index, strategy, neighbours, edge_weights, pid, mu=0.001, iter=100, weightSize = 3, error_prob = 0, algo = "LMS", alpha = 0, beta = 1):
    data = {
        "sync": 0,
        "strategy": strategy,
        "neighbours": neighbours,
        "edge_weights": edge_weights,
        "mu": mu,
        "iter": iter,
        "weightSize": weightSize,
        "p_id": pid,
        "error_prob": error_prob,
        "algo": "LMS",
        "alpha": alpha,
        "beta": beta
    }
    payload = json.dumps(data)
    topic = "picow_sync_{}".format(index)
    client = MQTTClient()
    client.loop_start()
    client.publish(topic=topic, message=payload, retain=True)
    client.loop_stop()
    client.disconnect()
    print("Published data to {}".format(topic))

def sync_node(index):
    #make the nodes use sync variable to control loop
    data = {
        "sync": 1
    }
    payload = json.dumps(data)
    topic = "picow_sync_{}".format(index)
    client = MQTTClient()
    client.loop_start()
    client.publish(topic=topic, message=payload, retain=True)
    client.loop_stop()
    client.disconnect()
    print("Published data to {}".format(topic))

def clear_retained_messages(index):
    topic = "picow_sync_{}".format(index)
    client = MQTTClient()
    client.loop_start()
    client.publish(topic=topic, message="", retain=True)
    client.loop_stop()
    client.disconnect()
    print("Cleared all retained messages in {}".format(topic))

generate_ne_we_data(2)