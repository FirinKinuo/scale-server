from aiohttp import web

from app.web import controllers

transmission_routes = [
    web.get(r'/{com:\d*}', controllers.send_weight_data),
    web.get('/setp', controllers.set_weight_percent),
    web.get('/getp', controllers.get_weight_percent)
]

visual_routes = [
    web.get(r'/{com:\d*}', controllers.send_web_form)
]
