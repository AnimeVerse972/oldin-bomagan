from aiohttp import web
import threading

async def handle(request):
    return web.Response(text="Bot alive")

def keep_alive():
    app = web.Application()
    app.router.add_get("/", handle)
    threading.Thread(target=web._run_app, args=(app,), kwargs={"port": 8080}).start()
