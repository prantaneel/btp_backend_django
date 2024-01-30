import paho.mqtt.client as mqtt
import json, logging
import ssl
from .models import Device, Measurement, ConsolidatedMSE, Process  # Import your Django models
from django.conf import settings
#change measurement 
TOPIC = settings.MQTT_CENTRAL_TOPIC

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(TOPIC)
    print(client.is_connected())
    print(f"Django is connected to the topic {TOPIC}")
    # Subscribe to MQTT topics, if needed

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        device_id = payload['device_id']
        message_type = payload['message_type']
        p_id = payload['p_id'] #process ID
        process_valid = Process.objects.filter(p_id=p_id).exists()
        if process_valid == False:
            print("Not a valid process!")
            return
        process = Process.objects.get(p_id=p_id)
        if message_type == 'registration':
            # Create a new device
            print(device_id, message_type, payload)
            try:#
                device_available  = Device.objects.filter(device_id=device_id, process=process).exists()
                if device_available:
                    device = Device.objects.get(device_id=device_id, process=process)
                    print("Device is already available")
                else:
                    print("Device is not available")
                    device = Device(device_id=device_id, process=process)
                    measurement_init = Measurement(device=device, process=process, iteration=0, mse=0, low_cost_data=json.dumps([]), w_iter = json.dumps([]))
                    consolidated_mse = ConsolidatedMSE(device=device, process=process, iteration=0, mse_array =  json.dumps([{"iteration": 0, "mse": 0}]))
                    device.save()
                    measurement_init.save()
                    consolidated_mse.save()
            except Device.DoesNotExist:
                print("Device doesn't exist")

        elif message_type == 'update':
            # Find the device and create a measurement
            device_available  = Device.objects.filter(device_id=device_id, process=process).exists()
            if device_available:
                device = Device.objects.get(device_id=device_id, process=process)
                iteration = payload["iteration"]
                alr_ext = Measurement.objects.filter(device=device, process=process, iteration=iteration).exists()
                if alr_ext:
                    print("Dual Signal! Skipped!")
                else:
                    measurement_prev = Measurement.objects.get(device = device, process=process,iteration= iteration-1)
                    cmse = ConsolidatedMSE.objects.get(device=device, process=process)
                    cmse_arr = json.loads(cmse.mse_array)
                    mse_prev = measurement_prev.mse
                    high_cost_data = payload["high_cost_data"]
                    low_cost_data = payload["low_cost_data"]
                    w_iter = payload["w_iter"]
                    d_pred = 0
                    print(low_cost_data, w_iter)
                    for _iter in range(len(w_iter)):
                        d_pred = d_pred + low_cost_data[_iter]*w_iter[_iter]
                    mse_now = ((iteration - 1)*mse_prev + pow(high_cost_data - d_pred, 2))/iteration
                    cmse_arr.append({"mse":mse_now, "iteration": iteration})
                    cmse.iteration = iteration
                    cmse.mse_array = json.dumps(cmse_arr)
                    measurement = Measurement(device=device, process=process,iteration=payload["iteration"], high_cost_data=payload["high_cost_data"], low_cost_data = json.dumps(payload["low_cost_data"]), w_iter = json.dumps(payload["w_iter"]), mse = mse_now)
                    print(device_id, message_type, payload)
                    measurement.save()
                    cmse.save()
                    print("Measurement Recorded")
            else:
                logging.warning("Device is not available")
        
        elif message_type == 'completed':
            try:#
                device_available  = Device.objects.filter(device_id=device_id, process=process).exists()
                if device_available == False:
                    print("Device is not available")
                else:
                    print("Training Completed for {}".format(device_id))
                    device = Device.objects.get(device_id=device_id, process=process)
                    cmse = ConsolidatedMSE.objects.get(device=device, process=process)
                    print(cmse.mse_array)
                    device.completed = True
                    device.save()
            except Device.DoesNotExist:
                print("Device doesn't exist")

    except json.JSONDecodeError:
        # The message is not valid JSON
        print(f"Received a non-JSON message on topic {message.topic}: {message.payload.decode()}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)  # Enforce TLS 1.2 or newer
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
