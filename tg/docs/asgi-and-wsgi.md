# ASGI and WSGI entry points

This page describes the two server entry points in the `tg` package,
[`tg/asgi.py`](../asgi.py) and [`tg/wsgi.py`](../wsgi.py): what each application object
serves and how WebSocket connections reach the scene chat. It is for developers running
the server and operators deploying it. The realtime design itself is in
[scenes and realtime](../../docs/architecture/scenes-and-realtime.md).

## ASGI: `tg.asgi.application`

The project is an ASGI application built with [Django Channels](https://channels.readthedocs.io/).
`settings.ASGI_APPLICATION` is `"tg.asgi.application"`.

`asgi.py`:

1. sets `DJANGO_SETTINGS_MODULE` to `tg.settings` if it is unset;
2. calls `django.core.asgi.get_asgi_application()` first, which sets Django up, and only
   then imports `game.routing` (importing consumers earlier would load models before the
   app registry is ready);
3. builds a `channels.routing.ProtocolTypeRouter`:

| Protocol | Handled by |
|----------|------------|
| `http` | The Django ASGI application: the full middleware stack, URLconf and views |
| `websocket` | `AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))` |

For WebSockets:

- `AllowedHostsOriginValidator` rejects connections whose `Origin` header does not match
  `ALLOWED_HOSTS`. (The development settings leave `[::1]` out of the default
  `ALLOWED_HOSTS` for this reason; see [settings](settings.md#developmentpy).)
- `AuthMiddlewareStack` reads the session cookie and puts the Django user in
  `scope["user"]`.
- `URLRouter` dispatches `game.routing.websocket_urlpatterns`, which has one route:
  `ws/scene/<scene_id>/` to `game.consumers.SceneChatConsumer`.

The HTTP route policies in `core` do not apply to WebSocket connections; the consumer
checks the user's access to the scene itself (see the [game app](../../game/README.md)).

The channel layer that carries messages between consumers is `InMemoryChannelLayer` in
development (single process) and `channels_redis` in production (`REDIS_URL`); see
[settings](settings.md).

### Running it

`daphne` is the first entry in `INSTALLED_APPS`, so its `runserver` command replaces
Django's and serves the ASGI application, WebSockets included:

```bash
python manage.py runserver 7000
```

In production run an ASGI server against `tg.asgi:application` (the pinned `daphne`
package provides one), with `DJANGO_ENVIRONMENT=production` and the production
variables set. See [deployment](../../docs/operations/deployment.md).

## WSGI: `tg.wsgi.application`

`wsgi.py` sets `DJANGO_SETTINGS_MODULE` to `tg.settings` if unset and exposes
`django.core.wsgi.get_wsgi_application()`. `settings.WSGI_APPLICATION` points at it. A
WSGI server serves HTTP only: scene pages still load, but live scene updates over
WebSockets do not work under WSGI.

## See also

- [Scenes and realtime](../../docs/architecture/scenes-and-realtime.md)
- [Deployment](../../docs/operations/deployment.md)
- [Settings](settings.md)
- [game app](../../game/README.md)
- [`tg/asgi.py`](../asgi.py)
