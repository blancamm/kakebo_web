from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config') #es decir la configuracion de la aplicacion se hace desde fuera con el fichero config.py

import kakebo.views