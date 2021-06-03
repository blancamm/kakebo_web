#FICHERO PARA AFINAR: ESTE PARA ENCAPSULAR EL ACCESO A LA BASE DE DATOS, Y ASÍ SE PUEDE MEJORAR ESTE SIN AFECTAR EL VIEWS

import sqlite3


class DBmanager():
    def __toDict__(self,cur):
        # Obtenemos los datos de la consulta  
        claves = cur.description 
        filas = cur.fetchall() 
                
        # Procesamos los datos/ registros en una lista de diccionarios
        resultado= []
        for fila in filas: 
            d = {}
            for tclave, valor in zip(claves,fila):
                d[tclave[0]]=valor
            resultado.append(d)

        return resultado

    def consultaMuchasSQL(self, query, parametros=[]):

        # Se abre la conexion
        conexion = sqlite3.connect('movimientos.db')
        cur=conexion.cursor()   

        # Se ejecuta la consulta
        cur.execute(query, parametros)
        resultado = self.__toDict__(cur)
        conexion.close()
        return resultado


    def consultaUnaSQL(self, query, parametros=[]):
        resultado = self.consultaMuchasSQL(query, parametros)
        if len(resultado) > 0:
            return resultado[0]

    def modificaSQL(self, query, parametros =[]):
        conexion = sqlite3.connect('movimientos.db')
        cur=conexion.cursor() 

        cur.execute(query, parametros)

        conexion.commit()
        conexion.close()
