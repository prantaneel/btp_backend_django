from .mqtt_client import MQTTClient
import json

network_graph = [
    [0.5, 0.25, 0.25, 0, 0, 0],
    [0.25, 0.5, 0.25, 0, 0, 0],
    [0.2, 0.2, 0.4, 0.2, 0, 0],
    [0, 0, 0.2, 0.4, 0.2, 0.2],
    [0, 0, 0, 0.25, 0.5, 0.25],
    [0, 0, 0, 0.25, 0.25, 0.5]
]
Number_of_nodes = 6



def generate_ne_we_data(index, graph=network_graph, N=Number_of_nodes, threshold = 0):
    neighbours = []
    edge_weights = []
    for _iter in range(N):
        if _iter==index:
            continue
        if graph[index][_iter] > threshold:
            neighbours.append(_iter)
            edge_weights.append(graph[index][_iter])
    edge_weights.append(graph[index][index])
    return neighbours, edge_weights

def publish_ne_we_data(index, strategy, neighbours, edge_weights, pid, mu=0.001, iter=100, weightSize = 3):
    data = {
        "sync": 0, 
        "strategy": strategy,
        "neighbours": neighbours,
        "edge_weights": edge_weights,
        "mu": mu,
        "iter": iter,
        "weightSize": weightSize,
        "p_id": pid     
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
    