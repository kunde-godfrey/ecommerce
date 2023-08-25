import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print(self.room_name)
        #Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.room_name
        )
        print('Connected')

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.room_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        print(self.room_group_name)
        print(self.room_name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

        print('sent')



    def chat_message(self, event):
        message = event["message"]
        print('about to call')
        self.send(text_data=json.dumps({"message": message}))
        print('Called')