from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_name>\w+)/$', consumers.GameDetailConsumer.as_asgi()),
    re_path(r'ws/session/', consumers.GameConsumer.as_asgi()),
]