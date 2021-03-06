from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for, flash #flash para mandar mensajes genericos
from kakebo.dataaccess import *
from kakebo.forms import FiltarMovimientos, MovimientosForm
from datetime import date

dbManager= DBmanager() #como es una clase, tengo que instanciarla

@app.route('/', methods=['GET', 'POST'])
def index():

    filtraform=FiltarMovimientos()  #asi te instancia le formulario con los datos de entrada
    #el formulario solo viaje en un post, no en un get, por lo que hay que meterle , inicializar el formulario
    #con los datos de entrada

    parametros = []
    query= "SELECT * FROM movimientos WHERE 1=1" #el where 1=1 se pone para que te deje poner un AND (pero ponemos una condicion que siempre es cierta 1=1 siempre es verdadero)
    
    if request.method=='POST':

        if filtraform.validate():   
            if filtraform.fechaDesde.data != None:#o sea que se ha informado de algo y no esta vacio
                query += " AND fecha >= ?" 
                parametros.append(filtraform.fechaDesde.data)
            if filtraform.fechaHasta.data != None:
                query += " AND fecha <= ?"
                parametros.append(filtraform.fechaHasta.data)
            if filtraform.texto.data != '':
                query += ' AND concepto LIKE ?' #METER ESTO ESTO EN EL ORDENADOR EL SIMBOLO % PARA QUE APAREZCA ALGO EN ESE HUECO DONDE ESTA %
                parametros.append("%{}%".format(filtraform.texto.data))

    query += " ORDER BY fecha" #queremos ordenarlos por fache dandonos igual si es GET Y POST. ORDER BY SIEMPRE TIENE QUE SER LA ULTIMA ORDEN SIEMPRE.
    print(query)
    movimientos=dbManager.consultaMuchasSQL(query, parametros) #siempre te tiene que hacer los movimientos con el query que toque, para que se use en el return

    # ya no es necesaria la siguiente linea, porque si no se pone una fecha para filtrar, te da
    # todos los movimientos segun esta instruccion que simepre es cierta query= "SELECT * FROM movimientos WHERE 1=1" que esta arriba y que sustitye a 
    #movimientos= consultaSQL('SELECT * FROM movimientos;').  Adem??s, si no metemos unos filtros (un post) queremos que nos devulve la render template
    saldo = 0
    for diccionario in movimientos:

        if diccionario['esGasto']== 0:
            saldo = saldo + diccionario['cantidad']
        elif diccionario['esGasto']== 1:
            saldo = saldo - diccionario['cantidad']
        
        diccionario['saldo']= saldo

    #EL RETURN ESTA FUERA DEL POST PORQUE ES UN FILTRO Y QUEREMOS INFORMACION, HACEMOS UN GET

    return render_template('movimientos.html', datos=movimientos, formulario = filtraform)

@app.route("/nuevo", methods= ['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form= formulario)
    else:
        if formulario.validate(): #esto es un metodo del formulario flask en el que llama a los validators 
            
            query = """
            INSERT INTO Movimientos  (fecha, concepto, categoria, esGasto, cantidad)
            VALUES (?, ?, ?, ?, ?)
            """  
            #se va a inyectar query en squlite y por eso se pone en ese lengauje
            #comentarios = es una cadena en linea, para ponerlo en varios lineas se usan las tres comillas, 
            #se podria utilizar '' pero no se podria divir en lineas
            #para informar a sqlite de que es avriable lo que se metge es poner el signo ?
            #tambien en vez de ? se puede poner :concepto, :categoria, ... y en execute se pone en vez
            #de una lista, un diccionario tipo 'fecha': formulario.fecha.data, ....
            #si es true, es que no hay errores (el if de formulario.validate())
            #SE BUSCAN LOS COMANDOS DEL SQLITE

            #hay que controlar los errores de accesos

            try:
                dbManager.modificaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error:
                print('Error en SQL INSERT' , el_error)
                flash('Se ha producido un error en la base de datos. Pruebe en unos minutos.') #ahora se prepara la plantilla 'base.html' para este flash que es generico (el flash lo que hace es que este mensaje este disponbible para el html)
                return render_template('alta.html', form= formulario)
            

            return redirect(url_for('index'))

        else:
            return render_template('alta.html', form= formulario)

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        registro= dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?;", [id])
        if not registro: #por si acaso alguien ya ha borrado el registro
            flash('El registro no existe', 'error')
            return render_template('borrar.html', movimiento= {})

        return render_template('borrar.html', movimiento=registro)
    
    else:
        try:
            dbManager.modificaSQL("DELETE FROM movimientos WHERE id=?;", [id])
        except sqlite3.error as e:
            flash('Se ha producido un error en la base de datos. Pruebe en unos minutos.', 'error')
            return redirect(url_for('index'))

        flash('Borrado realizado con exito', 'aviso') #le hemos metido categoria error/aviso para que sean diferente
        return redirect(url_for('index'))


    ''' 
    Esto funciona porque para llegar a esta route, se parte de movimientos, donde el cursor
    tiene toda la informaci??n. Entonces en el html de movimientos esta la info de identificador
    (porque lo tiene guardado el cursor) por lo que con esa info se pone en la route /borrar/id. 
    Ahora esa nueva route con su funcion, tiene la info del id porque viene en la ruta 
    entre <> y eso se lo guardaba. Por loq eu esa info (el id) se guarda para la funcion
    def borrar(id) y se puede utilizar en su return
    '''    

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method== 'GET':
        registro= dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?;", [id])
        if not registro: 
            flash('El registro no existe', 'error')
            return render_template('modificar.html', form=MovimientosForm())

        #como la data cogida de la fila[0] (que es un diccionario con ese registro) 
        #nos da la fecha en el formato incorrecto, se hace lo siguiente:
        registro['fecha']= date.fromisoformat(registro['fecha'])

        formulario = MovimientosForm(data=registro) #esto es para crear el formulario pero ya con los datos puestos del registro que vamos a modicar

        return render_template('modificar.html', form=formulario)
        #en el html. pongo form, porque le paso ese formulario que es el formulario con 
        #los valores del registro

    else:
        formulario = MovimientosForm() #si no dice na coge el formulario que ha entrado, el de request.form
        #es la info que viene del navegador no del servidor por eso no se tomo el formulario de lo de arriba del metodo get
        
        if formulario.validate():
            query = "UPDATE movimientos SET fecha=?, concepto=?, categoria=?, esGasto=?, cantidad=? WHERE id=?;"
            try:
                dbManager.modificaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                    formulario.esGasto.data, formulario.cantidad.data, id]) #formulario porque es instancia de Movimeintos form que tiene fecha \
                                    #que es una instancia de la clase Field con atributo data
                
                flash('Modificaci??n realizada con ??xito', 'aviso') #para que los escriba en eol navegador y no en el terminal (en el servidor)
                return redirect(url_for('index')) 
            
            except sqlite3.Error as e:
                flash('Se ha producido un error de base de datos, vuelva a intentarlo', 'error')
                return render_template('modificar.html', form=formulario)

        else:
            return render_template('modificar.html', form = formulario)
   

@app.route('/deberes')
def deberes():
    campos= ('Nombre', 'Apellidos', 'Matem??ticas', 'Lengua','Naturales', 'Sociales')
    personas= [('Pedro', 'Jimenez', 10, 9, 8, 9),('Juana', 'Rodr??guez', 9, 4, 9, 8),('Andr??s', 'Stevensson', 6, 7, 9, 5)]

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
