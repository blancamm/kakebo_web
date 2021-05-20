from flask import Flask #Flask va a ser una clase que va a ser la aplicacion Flask (se instancia una sola vez)


app = Flask(__name__) #tiene que llevar un indicador, es el nombre del fichero en este caso

@app.route('/') #el decorador

def index():
    return 'Hola, mundo!'

@app.route('/adios')
def bye():
    return 'Hasta luego cocodrilo'


