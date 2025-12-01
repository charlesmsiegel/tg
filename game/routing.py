"""
WebSocket URL routing for the game app.
"""

from django.urls import re_path
from game.consumers import SceneChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/scene/(?P<scene_id>\d+)/$", SceneChatConsumer.as_asgi()),
]
