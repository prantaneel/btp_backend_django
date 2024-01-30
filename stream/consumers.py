import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.node_id = self.scope["url_route"]["kwargs"]["node_id"]
        self.group_name = f"{self.node_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.send(text_data=json.dumps({"message": message}))
        
    async def device_created(self, event):
        await self.send(text_data=json.dumps({
            'event': 'device.created',
            'device_id': event['device_id'],
            "p_id": event['p_id'],
            "completed": event["completed"]
        }))

    async def measurement_created(self, event):
        await self.send(text_data=json.dumps({
            'event': 'measurement.created',
            'device_id': event['device_id'],
            'iteration': event['iteration'],
            'mse': event['mse']
        }))
    async def device_completed(self, event):
        await self.send(text_data=json.dumps({
            'event': 'device.completed',
            'device_id': event['device_id'],
            "p_id": event['p_id'],
            "completed": event["completed"],
            "cmse": event["cmse"]
        }))

    async def device_deleted(self, event):
        await self.send(text_data=json.dumps({
            'event': 'device.deleted',
            'device_id': event['device_id'],
        }))

    pass
