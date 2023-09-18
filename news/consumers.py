from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class NewsConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("broadcast", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("broadcast", self.channel_name)

    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            "broadcast",
            {"type": "news_post_added", **content},
        )

    def news_post_added(self, event):
        self.send_json(event)
