
from flask import jsonify, render_template
from kakebo import app
import sqlite3
from kakebo.forms import MovimientosForm

@app.route('/')
def index():
    conexion = sqlite3.connect('movimientos.db')
    cur=conexion.cursor()

    cur.execute('SELECT * FROM movimientos;') #se los guarda el cursor (saca los datos)
    
    claves = cur.description #TE DA LAS TUPLAS DE DESCRIPCION
    filas = cur.fetchall() #TODAS LAS FILAS DE LOS REGISTROS

    movimientos= []
    saldo = 0
    for fila in filas: #cada fila es un registro con sus atributos
        d = {}
        for tclave, valor in zip(claves,fila): #cada atributo es la clave
            d[tclave[0]]=valor
        
        if d['esGasto']== 0:
            saldo += d['cantidad']
        elif d['esGasto']== 1:
            saldo -=d['cantidad']
        
        d['saldo']= saldo

        movimientos.append(d)
        
    conexion.close()

    return render_template('movimientos.html', datos=movimientos) #voy a meter los movimientos que son los registros según lo de arriba

@app.route("/nuevo", methods= ['GET', 'POST'])
def nuevo():
    form = MovimientosForm()
    return render_template('alta.html', form= form)

@app.route('/deberes')
def deberes():
    campos= ('Nombre', 'Apellidos', 'Matemáticas', 'Lengua','Naturales', 'Sociales')
    personas= [('Pedro', 'Jimenez', 10, 9, 8, 9),('Juana', 'Rodríguez', 9, 4, 9, 8),('Andrés', 'Stevensson', 6, 7, 9, 5)]

    boletines=[]
    for alumno in personas:
        diccionario= {}
        sumatorio = 0
        denominador = 0
        for indice in range (0,len(alumno)): #se prodria utilizar el enumerate
            diccionario[campos[indice]]= alumno[indice]

        #OTRA FORMA, MAS VISUAL:
        '''
        for clave, valor in zip(campos, alumno):
            diccionario[clave]= valor
        '''
            
        esNumero = alumno[indice]
        try:
                esNumero == int(esNumero)
                sumatorio += alumno[indice]
                denominador += 1

        except:
                pass
        
        media = sumatorio/denominador
        diccionario['media'] = media

        num_estrellas = media // 0.5
        resto = media % 0.5

        if resto != 0:
            num_estrellas +=1

        grafico = int(num_estrellas) * '*'
        diccionario['grafico'] = grafico
        boletines.append(diccionario)

    return jsonify(boletines)
