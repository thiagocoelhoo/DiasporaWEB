import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from myapp import models


class ArduinoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.accpet()

    async def receive(self, text_data):
        """
        Tem que ser verificado se as informações enviadas 
        estão ou não corretas. É importante também realizar
        a  higienização dos dados.
        """

        text_data_json = json.loads(text_data)
        gas = text_data_json.get('gas')
        temp = text_data_json.get('temp')
        
        if not (gas and temp):
            return 
        
        await self.channel_layer.group_send(
            'notifications',
            {
                'type': 'notify_all',
                'message': text_data
            }
        )

        await self.save_sensordata(gas, temp)

    @database_sync_to_async
    def save_sensordata(self, gas, temp):
        models.SensorData.objects.create(gas=gas, temp=temp)


class NotifycationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if not user.is_authenticated:
            return await self.close()
        
        self.group_name = 'notifications'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )
    
    async def notify_all(self, event):
        await self.send(text_data=event['message'])


class VideoStreamConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'videostream_group'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'message': text_data_json,
                'destination_channel': self.channel_name
            }
        )
    
    async def message(self, event):
        if event['destination_channel'] != self.channel_name:
            message = json.dumps(event['message'])
            await self.send(text_data=message)
