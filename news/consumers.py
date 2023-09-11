from channels.generic.websocket import JsonWebsocketConsumer


class NewsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        self.send_json(
            {"title": f"Добавлена новость \"{content.get('title', 'Без названия')}\""}
        )
