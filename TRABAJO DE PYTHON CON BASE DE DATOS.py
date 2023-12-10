# Conocer los conceptos de clases, objetos y métodos, adquiriendo competencias en el diseño e implementación
# de bases de datos relacionales y ponerlos en prácticas con el lenguaje de programación Python

# IMPORTANTE: Instalar las librerias time, datetime, prettytable, mysql.connector y ejecutar el archivo .sql
# adjunto en la carpeta [S14-TRABAJO PRACTICO EXPERIMENTAL_2 POO] para que el programa funcione correctamente

from time import sleep
from datetime import datetime, timedelta
import mysql.connector
from prettytable import PrettyTable
from mysql.connector import connect


class Conexion:
    def __init__(self):  # conectarse a la base de datos y validar la conexion si se llega a interrumpir
        cont = 0
        cont2 = 0
        while True:
            try:
                self.connection = connect(user="User_prueba", password="User_prueb@_2023",
                                          database="sistema de biblioteca", host="127.0.0.1")
                self.cursor = self.connection.cursor()
                if cont2 > 0:
                    print("Conexión Establecida")
                    cont2 = 0
                break
            except mysql.connector.Error as e:
                print(f"No se ha podido establecer conección con la base de datos\n{e}\nReintentando....")
                sleep(1)
                cont += 1
                cont2 += 1
                if cont == 3:
                    print("No se Puede conectar con la base de datos por favor revise su Servidor MySQL")
                    print("Presione 1 para volver a intentar conectarse a la base de datos ")
                    while True:
                        try:
                            value_extra = int(validate_num())  # llamar a la función validate_num()
                            if value_extra == 1:
                                break
                            else:
                                print("Ingrese el número 1")
                        except ValueError:
                            print("Ingrese un número válido")

    def fetch_all(self, query):  # devolver cadena de tupas
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, parms):  # devolver tupla con 1 valor
        self.cursor.execute(query, parms)
        return self.cursor.fetchone()

    def delete(self, query, parms):  # borrar un objeto en la base de datos
        try:
            self.cursor.execute(query, parms)
            self.connection.commit()
        except mysql.connector.Error as e:
            print('Error:', e)

    def update(self, query, parms):  # actualizar un objeto en la base de datos
        try:
            self.cursor.execute(query, parms)
            self.connection.commit()
        except mysql.connector.Error as e:
            print('Error:', e)

    def insert(self, query, parms):  # insertar un objeto en la base de datos
        try:
            self.cursor.execute(query, parms)
            self.connection.commit()
        except mysql.connector.IntegrityError as e:
            print('Error:', e)

    def cerrar_conexion(self):  # cerrar coneccion con la base de datos
        self.cursor.close()
        self.connection.close()


class Authors:
    def __init__(self,  id_author, name, last_name, birthdate):
        self.id_authors = id_author
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate

    @staticmethod
    def validate_nombres(name, last_name):  # validar que no existan los nombres del autor
        db = Conexion()
        query = "SELECT COUNT(*) FROM author WHERE NOMBRES = %s AND APELLIDOS = %s;"
        result = db.fetch_one(query, (name, last_name))[0]
        db.cerrar_conexion()
        if int(result) == 1:
            return False
        return True

    @staticmethod
    def validate_id(cod):  # validar que no existan el codigo del autor
        db = Conexion()
        query = "SELECT COUNT(*) FROM author WHERE ID_AUTHOR = %s;"
        result = db.fetch_one(query, (cod,))[0]
        db.cerrar_conexion()
        if int(result) == 1:
            return False
        return True

    @staticmethod
    def check_register():  # verificar que existan registros de autores
        db = Conexion()
        query = "SELECT COUNT(*) FROM author;"
        result = db.fetch_all(query)
        db.cerrar_conexion()
        result = result[0][0]
        if int(result) > 0:
            return False
        return True

    def create_autor(self):  # crear autor en la base de datos
        db = Conexion()
        query = "INSERT INTO author (ID_AUTHOR, NOMBRES, APELLIDOS, FECHA_NACIMIENTO) VALUES (%s, %s, %s, %s);"
        db.insert(query, (self.id_authors, self.name, self.last_name, self.birthdate))
        db.cerrar_conexion()

    @staticmethod
    def list_all():  # listar a todos los autores y presentarlos por pantalla
        db = Conexion()
        query = "SELECT * FROM author;"
        data = db.fetch_all(query)
        db.cerrar_conexion()
        tabla = PrettyTable()
        tabla.field_names = ["ID de Autor", "Nombres", "Apellidos", "Fecha de Nacimiento"]
        for author in data:
            tabla.add_row([author[0], author[1], author[2], author[3]])
        print(tabla)
        sleep(4)

    def consult_author(self, values):  # consultar autor por su codigo y devolver su codigo
        tabla = PrettyTable()
        tabla.field_names = ["ID de Autor", "Nombres", "Apellidos", "Fecha de Nacimiento"]
        print("Ingrese el Código del Autor")
        while True:
            cod = validate_cod().upper()
            if not(self.validate_id(cod)):
                db = Conexion()
                query = f"SELECT * FROM author WHERE ID_AUTHOR = '{cod}';"
                data = db.fetch_all(query)
                db.cerrar_conexion()
                for author in data:
                    tabla.add_row([author[0], author[1], author[2], author[3]])
                print(tabla)
                sleep(2)
                if values == 1:
                    return None
                elif values == 2:
                    print("Desea Agregar a este Autor a su Libro\n1.Si\n2.No")
                    value = validate_operator(2)
                    if value == 1:
                        return str(data[0][0])
                    else:
                        print("Volver a Ingresar el Código del Autor")
                elif values == 3:
                    return cod
            else:
                print("El Código del Autor es incorrecto, ingrese un Código válido")

    def consult_author_name(self):  # consultar autor por su nombre
        tabla = PrettyTable()
        tabla.field_names = ["ID de Autor", "Nombres", "Apellidos", "Fecha de Nacimiento"]
        while True:
            print("Ingrese los Nombres del Author")
            name = validate_words(1).upper()
            print("Ingrese los Apellidos del Author")
            last_name = validate_words(1).upper()
            if self.validate_nombres(name, last_name):
                print("El Nombre del Autor es incorrecto o esta mal escrito, ingrese nuevamente")
            else:
                break
        db = Conexion()
        query = f"SELECT * FROM author WHERE NOMBRES = '{name}' AND APELLIDOS = '{last_name}';"
        data = db.fetch_all(query)
        db.cerrar_conexion()
        for author in data:
            tabla.add_row([author[0], author[1], author[2], author[3]])
        print(tabla)
        sleep(2)

    def modify_author_info(self, value_2, cod):  # modificar autor en partes dependiendo del valor de value2
        if value_2 == 1:
            print("Ingrese el Nuevo Código del Autor")
            while True:
                new_cod = validate_cod().upper()
                if self.validate_id(new_cod):
                    break
                else:
                    print("El Código ya existe")
            db = Conexion()
            query2 = "UPDATE author SET ID_AUTHOR=%s WHERE ID_AUTHOR=%s;"
            db.update(query2, (new_cod, cod))
            db.cerrar_conexion()
        elif value_2 == 2:
            while True:
                print("Ingrese los Nuevos Nombres del Author")
                new_name = validate_words(1).upper()
                print("Ingrese los Apellidos del Author")
                new_last_name = validate_words(1).upper()
                if self.validate_nombres(new_name, new_last_name):
                    break
                else:
                    print("El Nombre del Autor ya existe, ingrese nuevamente")
            db = Conexion()
            query2 = "UPDATE author SET NOMBRES=%s, APELLIDOS=%s WHERE ID_AUTHOR=%s;"
            db.update(query2, (new_name, new_last_name, cod))
            db.cerrar_conexion()
        elif value_2 == 3:
            print("Ingrese su Nueva Fecha de Nacimiento: ")
            while True:
                new_birthdate = str(validate_date())
                if self.validate_how_many_books(cod):
                    if self.validate_date_author(new_birthdate, cod):
                        break
                else:
                    break
            db = Conexion()
            query2 = "UPDATE author SET FECHA_NACIMIENTO=%s WHERE ID_AUTHOR=%s;"
            db.update(query2, (new_birthdate, cod))
            db.cerrar_conexion()

    @staticmethod
    def validate_how_many_books(cod):  # consultar cuantos libros tiene un author
        db = Conexion()
        query = "SELECT COUNT(*) FROM book WHERE ID_AUTHOR = %s;"
        data = db.fetch_one(query, (cod,))[0]
        db.cerrar_conexion()
        if int(data) > 0:
            return True
        return False

    @staticmethod
    def validate_date_author(fecha, cod):  # validar la fecha de publicacion del primer libro asignado al author
        db = Conexion()
        query = f"SELECT book.FECHA_PUBLICACION FROM book WHERE ID_AUTHOR = {cod};"
        data = [datetime.strptime(str(row[0]), "%Y-%m-%d") for row in db.fetch_all(query)]
        db.cerrar_conexion()
        data_or = sorted(data, reverse=False)
        data = data_or[0]
        data2 = datetime.strptime(fecha, "%Y-%m-%d")
        if data > data2:
            if data2 + timedelta(days=18*365) < data:
                return True
            print("El autor es menor de edad con respecto a la fecha de publicación")
            print("de su primer Libro, ingrese una Fecha correcta")
        else:
            print("La Fecha de Nacimiento del Autor tiene que ser menor a la fecha de publicación")
            print("de su primer Libro, ingrese una Fecha correcta")
            return False

    def delete_author(self):  # eliminar autor y sus libros asociados
        cod = self.consult_author(3)
        print("Desea Eliminar la Información del autor\nSi Elimina La Información se eliminaran los libros asociados "
              "al Autor\n1.Si\n2.No (Volver al Menú)")
        value = validate_operator(2)
        if value == 1:
            db = Conexion()
            query = "DELETE FROM author WHERE ID_AUTHOR = %s;"
            db.delete(query, (cod,))
            query2 = "DELETE FROM book WHERE ID_AUTHOR = %s;"
            db.delete(query2, (cod,))
            db.cerrar_conexion()
            return True
        return False


class Books:
    def __init__(self,  id_book, name, publication_date, id_author):
        self.id_book = id_book
        self.name = name
        self.publication_date = publication_date
        self.id_authors = id_author

    @staticmethod
    def validate_nombres(nom):  # validar que no existan los nombres del libro
        db = Conexion()
        query = "SELECT COUNT(*) FROM book WHERE TITULO = %s;"
        data = db.fetch_one(query, (nom,))[0]
        db.cerrar_conexion()
        if int(data) == 1:
            return False
        return True

    @staticmethod
    def validate_id(cod):  # validar que no exista el codigo del libro
        db = Conexion()
        query = "SELECT COUNT(*) FROM book WHERE ID_BOOK = %s;"
        data = db.fetch_one(query, (cod,))[0]
        db.cerrar_conexion()
        if int(data) == 1:
            return False
        return True

    @staticmethod
    def check_prequel_or_sequel(value):  # verificar que existen libros con precuelas o secuelas
        if value == 1:
            word = "No Posee Secuela"
            db = Conexion()
            query = "SELECT COUNT(*) FROM book WHERE SECUELA != %s;"
            data = db.fetch_one(query, (word,))[0]
            db.cerrar_conexion()
            if int(data) == 0:
                return False
            return True
        elif value == 2:
            word = "No Posee Precuela"
            db = Conexion()
            query = "SELECT COUNT(*) FROM book WHERE PRECUELA != %s;"
            data = db.fetch_one(query, (word,))[0]
            db.cerrar_conexion()
            if int(data) == 0:
                return False
            return True

    def create_libro(self):  # crear libro en la base de datos
        db = Conexion()
        query = "INSERT INTO book (ID_BOOK, TITULO, FECHA_PUBLICACION, ID_AUTHOR) VALUES (%s, %s, %s, %s);"
        db.insert(query, (self.id_book, self.name, self.publication_date, self.id_authors))
        db.cerrar_conexion()

    @staticmethod
    def list_all():  # listar todos los libros y mostralos por pantalla
        db = Conexion()
        query = "SELECT * FROM book;"
        data = db.fetch_all(query)
        db.cerrar_conexion()
        tabla = PrettyTable()
        tabla.field_names = ["ID de Libro", "Título", "Fecha de Publicación", "ID de Autor", "SECUELA", "PRECUELA"]
        for book in data:
            tabla.add_row([book[0], book[1], book[2], book[3], book[4], book[5]])
        print(tabla)
        sleep(4)

    @staticmethod
    def consult_update(cod):  # atraves del codigo del libro devuelve el codigo del autor
        db = Conexion()
        query3 = "SELECT book.ID_AUTHOR FROM book WHERE ID_BOOK = %s;"
        cod3 = db.fetch_one(query3, (cod,))[0]
        db.cerrar_conexion()
        cod3 = cod3
        return cod3

    def consult_book_name(self):  # consulta libro por su titulo y devuelve el titulo
        tabla = PrettyTable()
        tabla.field_names = ["ID de Libro", "Título", "Fecha de Publicación", "ID de Autor", "SECUELA", "PRECUELA"]
        print("Ingrese el Título del Libro")
        while True:
            name = validate_words(2).upper()
            if not(self.validate_nombres(name)):
                db = Conexion()
                query = f"SELECT * FROM book WHERE TITULO = '{name}';"
                data = db.fetch_all(query)
                db.cerrar_conexion()
                for book in data:
                    tabla.add_row([book[0], book[1], book[2], book[3], book[4], book[5]])
                print(tabla)
                sleep(2)
                return name
            else:
                print("El Título del Libro es incorrecto, ingrese un Título válido")

    @staticmethod
    def validate_date(fecha, cod):  # Se valida que el autor sea mayor de edad para punblicar un libro
        db = Conexion()
        query = "SELECT author.FECHA_NACIMIENTO FROM author WHERE ID_AUTHOR = %s;"
        data = str(db.fetch_one(query, (cod,))[0])
        db.cerrar_conexion()
        data = datetime.strptime(data, "%Y-%m-%d")
        data2 = datetime.strptime(fecha, "%Y-%m-%d")
        if data < data2:
            if data + timedelta(days=18*365) < data2:
                return True
            print("La Fecha de Publicación no coincide con la Edad Adulta del Author\nIngrese una Fecha correcta")
            return False
        print("La Fecha de Publicación no coincide con la Fecha de Nacimiento del Autor\nIngrese una Fecha correcta")
        return False

    def validate_publication_date(self, cod):  # Se valida que la fecha de publicacion de una secuela o precuela
        while True:                      # sea mayor a la fecha de publicacion del libro al que se le quiere asignar
            print("Ingrese su Fecha de Publicación: ")
            new_publication_date = str(validate_date())
            if self.validate_date(new_publication_date, cod3):
                db = Conexion()
                query4 = "SELECT book.FECHA_PUBLICACION FROM book WHERE ID_BOOK = %s;"
                fecha = str(db.fetch_one(query4, (cod,))[0])
                db.cerrar_conexion()
                data = datetime.strptime(fecha, "%Y-%m-%d")
                data2 = datetime.strptime(new_publication_date, "%Y-%m-%d")
                if data < data2:
                    return new_publication_date
                print("La Fecha de Publicación de la Secuela o Precuela es incorrecta")

    @staticmethod
    def consult_title_book(cod):  # atraves del codigo del libro devuelve el titulo del libro
        db = Conexion()
        query = "SELECT book.TITULO FROM book WHERE ID_BOOK = %s;"
        cod2 = str(db.fetch_one(query, (cod,))[0])
        db.cerrar_conexion()
        return cod2

    @staticmethod
    def check_register(value=0):  # verificar que existan registros de autores
        db = Conexion()
        query = "SELECT COUNT(*) FROM book;"
        result = db.fetch_all(query)
        db.cerrar_conexion()
        result = result[0][0]
        if int(result) > value:
            return False
        return True

    @staticmethod
    def consult_prequel_or_sequel(name, word):  # consulta las precuelas o secuelas de un libro y lo imprime por
        con = 0                                       # pantalla
        tabla = PrettyTable()
        tabla.field_names = ["ID de Libro", "Título", "Fecha de Publicación", "ID de Autor", "SECUELA", "PRECUELA"]
        db = Conexion()
        query = f"SELECT book.{word} FROM book WHERE TITULO = '{name}';"
        cod = str(db.fetch_all(query))
        db.cerrar_conexion()
        nombres = cod.split(", ")
        for i in nombres:
            caracteres_a_eliminar = "(),[]',"
            tabla_de_traduccion = str.maketrans("", "", caracteres_a_eliminar)
            name2 = i.translate(tabla_de_traduccion)
            db = Conexion()
            query2 = f"SELECT * FROM book WHERE TITULO = '{name2}';"
            data = db.fetch_all(query2)
            db.cerrar_conexion()
            if name2 == "No Posee Precuela":
                print(name2)
                return None
            elif name2 == "No Posee Secuela":
                print(name2)
                return None
            else:
                con += 1
                for book in data:
                    tabla.add_row([book[0], book[1], book[2], book[3], book[4], book[5]])
        print(f"Existen {con} Libros asociados")
        print(tabla)
        sleep(2)

    def consult_book_id(self):  # consulta un libro por su codigo y devuelve el codigo
        tabla = PrettyTable()
        tabla.field_names = ["ID de Libro", "Título", "Fecha de Publicación", "ID de Autor", "SECUELA", "PRECUELA"]
        print("Ingrese el Código del Libro")
        while True:
            cod = validate_cod().upper()
            if not(self.validate_id(cod)):
                db = Conexion()
                query = f"SELECT * FROM book WHERE ID_BOOK = '{cod}';"
                data = db.fetch_all(query)
                db.cerrar_conexion()
                for book in data:
                    tabla.add_row([book[0], book[1], book[2], book[3], book[4], book[5]])
                print(tabla)
                sleep(2)
                return cod
            else:
                print("El Código del Libro es incorrecto, ingrese un Código válido")

    @staticmethod
    def consult_join():  # consulta un libro atraves de los nombres del autor (consulta join)
        while True:
            print("Ingrese los Nombres del Autor")
            name = validate_words(1).upper()
            print("Ingrese los Apellidos del Autor")
            last_name = validate_words(1).upper()
            if not(authors.validate_nombres(name, last_name)):
                db = Conexion()
                query = ("SELECT COUNT(*) FROM author JOIN book ON author.ID_AUTHOR = book.ID_AUTHOR "
                         "WHERE author.NOMBRES = %s AND author.APELLIDOS = %s;")
                id_book = int(db.fetch_one(query, (name, last_name))[0])
                db.cerrar_conexion()
                print(f"Existen {id_book} Libros asociados a este autor")
                tabla = PrettyTable()
                tabla.field_names = ["ID de Libro", "Titulo", "Fecha de Publicación", "ID de Autor", "SECUELA",
                                     "PRECUELA"]
                if id_book == 0:
                    print("EL autor no Posee Libros")
                    break
                else:
                    db = Conexion()
                    query2 = f"SELECT * FROM author JOIN book ON author.ID_AUTHOR = book.ID_AUTHOR " \
                             f"WHERE author.NOMBRES = '{name}' AND author.APELLIDOS = '{last_name}';"
                    data = db.fetch_all(query2)
                    db.cerrar_conexion()
                    for book in data:
                        tabla.add_row([book[4], book[5], book[6], book[7], book[8], book[9]])
                    print(tabla)
                    sleep(2)
                    break
            else:
                print("Los Nombres del Autor son incorrectos, Ingrese un Nombre Completo válido")

    @staticmethod
    def consult_data(publication_date, cod):  # se valida la entrada de la precuela o secuela
        db = Conexion()
        query = "SELECT book.FECHA_PUBLICACION FROM book WHERE ID_BOOK = %s;"
        fecha = str(db.fetch_one(query, (cod,))[0])
        db.cerrar_conexion()
        data = datetime.strptime(fecha, "%Y-%m-%d")
        data2 = datetime.strptime(publication_date, "%Y-%m-%d")
        if data < data2:
            db = Conexion()
            query2 = "UPDATE book SET FECHA_PUBLICACION=%s WHERE ID_BOOK=%s;"
            db.update(query2, (publication_date, cod))
            db.cerrar_conexion()
            return True
        else:
            print("La Fecha de Publicación de la Secuela o Precuela es incorrecta")
            return False

    def modify_book_info(self, value, value2, cod_b, cod_a=None, cod=None):  # modificar libro en partes dependiendo
        if value == 1:                                                       # del valor de value y modificar el
            print("Ingrese el Nuevo Código del Libro")                       # libro como una secuela o precuela
            while True:                                                      # dependiendo de value2
                new_cod = validate_cod().upper()
                if self.validate_id(new_cod):
                    break
                else:
                    print("El Código ya existe")
            db = Conexion()
            query2 = "UPDATE book SET ID_BOOK=%s WHERE ID_BOOK=%s;"
            db.update(query2, (new_cod, cod_b))
            db.cerrar_conexion()
            return new_cod
        elif value == 2:
            while True:
                print("Ingrese el Nuevo Titulo del Libro")
                new_name = validate_words(2).upper()
                if self.validate_nombres(new_name):
                    break
                print("El Título del Libro ya existe, ingrese nuevamente")
            db = Conexion()
            query2 = "UPDATE book SET TITULO=%s WHERE ID_BOOK=%s;"
            db.update(query2, (new_name, cod_b))
            db.cerrar_conexion()
            return new_name
        elif value == 3:
            if value2 == 1:
                print("Al Asignar un Libro como Secuela o Precuela se tiene que verificar su Fecha de Publicación")
            print("Ingrese su Fecha de Publicación: ")
            while True:
                new_publication_date = str(validate_date())
                if self.validate_date(new_publication_date, cod_a):
                    if value2 == 1:
                        if self.consult_data(new_publication_date, cod):
                            break
                    elif value2 == 2:
                        break
            db = Conexion()
            query2 = "UPDATE book SET FECHA_PUBLICACION=%s WHERE ID_BOOK=%s;"
            db.update(query2, (new_publication_date, cod_b))
            db.cerrar_conexion()
        else:
            print("Deseas Buscar o Agregar un Autor\n" + "1.Buscar\n2.Agregar")
            value_2 = validate_operator(2)
            if value_2 == 1:
                cod2 = authors.consult_author(2)
                new_id_author = cod2
            else:
                cod2 = create_author()
                new_id_author = cod2
            db = Conexion()
            query2 = "UPDATE book SET ID_AUTHOR=%s WHERE ID_BOOK=%s;"
            db.update(query2, (new_id_author, cod_b))
            db.cerrar_conexion()

    @staticmethod
    def enter_prequel_or_sequel(title, title2, cod, cod2):  # asignar el libro como precuela y secuela
        space = ", "
        print("Seleccionar el Libro como:\n1.Secuela\n2.Precula")
        value = validate_operator(2)
        while True:
            if value == 1:
                db = Conexion()
                query2 = "SELECT book.SECUELA FROM book WHERE ID_BOOK = %s;"
                data = str(db.fetch_one(query2, (cod,))[0])
                query3 = "SELECT book.PRECUELA FROM book WHERE ID_BOOK = %s;"
                data2 = str(db.fetch_one(query3, (cod2,))[0])
                if data == "No Posee Secuela":
                    query = "UPDATE book SET SECUELA=%s WHERE ID_BOOK=%s;"
                    db.update(query, (title, cod))
                else:
                    query = "UPDATE book SET SECUELA = CONCAT(%s, %s, %s) WHERE ID_BOOK = %s;"
                    db.update(query, (data, space, title, cod))
                if data2 == "No Posee Precuela":
                    query = "UPDATE book SET PRECUELA=%s WHERE ID_BOOK=%s;"
                    db.update(query, (title2, cod2))
                else:
                    query = "UPDATE book SET PRECUELA = CONCAT(%s, %s, %s) WHERE ID_BOOK = %s;"
                    db.update(query, (data2, space, title2, cod2))
                db.cerrar_conexion()
                break
            elif value == 2:
                title, title2, cod, cod2 = title2, title, cod2, cod
                value = 1

    def delete_book(self):  # eliminar libros
        cod = self.consult_book_id()
        if not(self.validate_id(cod)):
            print("Desea Eliminar la Información del Libro\n1.Si\n2.No (Volver al Menú)")
            value = validate_operator(2)
            if value == 1:
                db = Conexion()
                query = "DELETE FROM book WHERE ID_BOOK = %s;"
                db.delete(query, (cod,))
                db.cerrar_conexion()
                return True
        return False


def menu():  # funcion de menu
    print("+"+"-"*35+"+\n"+"|\t\tMenú De la Biblioteca\t\t|"+"\n| 1.Agregar Información"+" "*13+"|")
    print("| 2.Buscar Información\t"+" "*12+"|\n"+"| 3.Actualizar Información"+" "*10+"|")
    print("| 4.Eliminar Información"+" "*12+"|\n"+"| 5.Revisar Información"+" "*13+"|")
    print("| 6.Salir del Programa"+" "*14+"|\n+" + "-"*35+"+")
    print("Ingresar una opción ")
    value = validate_operator(6)
    return value


def validate_operator(i, j=1):  # validar numeros de j=1 hasta i
    print(f"Ingrese un valor entre {j} y {i}")
    while True:
        value = int(validate_num())  # llamar a la función validate_num()
        if j <= value <= i:
            break
        else:
            print("Ingrese un número que corresponda a las opciones del menú")
    return value


def validate_cod():  # validar la entrada de cualquier codigo ingresado
    cont = 0
    while True:
        try:
            print("El Código ingresado debe ser de tipo Alfanumérico ")
            values = str(input(">>"))  # pedir un dato
            for i in values:
                if not (i.isalpha() or i.isdigit()) and len(values) == 5:
                    cont += 1
            if cont > 0:
                print("El Código debe tener 5 digitos")
            else:
                break
        except ValueError:
            print("Ingrese un Código válido")  # Si el dato no se puede aceptar en el contexto actual repetir el proceso
    return values


def validate_num():  # función para validar el dato flotante y convertir en entero cuando se nesecite
    while True:
        try:
            values = float(input(">>"))  # pedir un dato
            break
        except ValueError:
            print("Ingrese un número válido")  # Si el dato no se puede aceptar en el contexto actual repetir el proceso
    return values


def validate_words(value):  # validar los nombres de los autores si value = 1 y los titulos de los libros si value = 2
    if value == 1:
        while True:
            cont = 0
            print("Los Nombres Ingresados seran convertidos a mayúsculas\nEjemplo: carlos --> CARLOS")
            values = str(input(">>"))  # pedir un dato
            for i in values:
                if not(i.isalpha() or i.isspace()):
                    cont += 1
            if cont > 0:
                print("Ingrese solo caracteres")
            else:
                break
        return values
    elif value == 2:
        while True:
            cont = 0
            print("Los Títulos Ingresados seran convertidos a mayúsculas\nEjemplo: el señor de los anillos --> "
                  "EL SEÑOR DE LOS ANILLOS")
            values = str(input(">>"))  # pedir un dato
            for i in values:
                if not(i.isalpha() or i.isspace() or i.isdigit()):
                    cont += 1
            if cont > 0:
                print("Ingrese solo caracteres")
            else:
                break
        return values


def validate_date():  # validar cada fecha ingresada y que no sobrepase la fecha actual
    while True:
        print("Día:")
        day = validate_operator(31)
        print("Mes:")
        month = validate_operator(12)
        print("Año:")
        years = validate_operator(2023, 1900)
        date = datetime(years, month, day)
        date_now = datetime.now()
        if date < date_now:
            date = str(date)
            date_corto = date[:10]
            return date_corto
        else:
            print("La Fecha es Incorrecta")


def create_author():  # crea autor atraves de validaciones sobre cada dato ingresado
    print("Ingrese el ID del Autor:")
    while True:
        cod = validate_cod().upper()
        if authors.validate_id(cod):
            break
        else:
            print("El Código ya existe")
    while True:
        print("Ingrese los Nombres del Author")
        name = validate_words(1).upper()
        print("Ingrese los Apellidos del Author")
        last_name = validate_words(1).upper()
        if authors.validate_nombres(name, last_name):
            break
        print("El Autor ya existe, ingrese nuevamente")
    print("Ingrese su Fecha de Nacimiento: ")
    birthdate = str(validate_date())
    author = Authors(cod, name, last_name, birthdate)
    author.create_autor()
    return cod


def create_libro(value):  # crea libro atraves de validaciones sobre cada dato ingresado
    cod2 = None
    value2 = 2
    if not(books.check_register()):
        print("Desea Ingresar el Libro como una Secuela o Precula de otro Libro\n1.Si\n2.No")
        value2 = validate_operator(2)
        if value2 == 1:
            print("Ingrese el Código del libro al que se le desea asignar una Secuela o Precuela")
            cod2 = books.consult_book_id()
            print("A continuación agregue la Información del Nuevo Libro")
    print("Ingrese el ID del Nuevo Libro:")
    while True:
        cod = validate_cod().upper()
        if books.validate_id(cod):
            break
        else:
            print("El Código ya existe")
    print("Ingrese el Nombre del Libro")
    while True:
        name = validate_words(2).upper()
        if books.validate_nombres(name):
            break
        print("El Libro ya existe, ingrese nuevamente")
    print("Ingrese la Fecha de publicación del Libro")
    while True:
        publication_date = str(validate_date())
        if books.validate_date(publication_date, value):
            if value2 == 1:
                if books.consult_data(publication_date, cod2):
                    break
            elif value2 == 2:
                break
    book = Books(cod, name, publication_date, value)
    book.create_libro()
    if value2 == 1:
        title = books.consult_title_book(cod2)
        books.enter_prequel_or_sequel(name, title, cod2, cod)


def menu_extra(word):  # menu para preguntar que deseas hacer con la opcion que elegiste del menu principal
    tabla = PrettyTable()
    tabla.field_names = [f"Qué Desea {word}"]
    tabla.add_row([f"1. {word} Autores"])
    tabla.add_row([f"2. {word} Libros"])
    tabla.add_row([f"3. Regresar al Menú"])
    print(tabla)


def create():  # validar la creacion de autores y libros, asi como su busqueda para asignarlos
    menu_extra("Agregar")
    value = validate_operator(3)
    if value == 1:
        cod = create_author()
        save()
        print("Desea Agregar un Libro al Autor\n"+"1.Si\n2.No")
        value_2 = validate_operator(2)
        if value_2 == 1:
            create_libro(cod)
        save()
    elif value == 2:
        print("Deseas Buscar o Agregar un Autor\n"+"1.Buscar\n2.Agregar")
        value_2 = validate_operator(2)
        if value_2 == 1:
            if authors.check_register():
                print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
            else:
                cod = authors.consult_author(2)
                create_libro(cod)
                save()
        else:
            cod = create_author()
            create_libro(cod)
            save()


def search():  # validar la busqueda de autores y libros
    menu_extra("Buscar")
    value = validate_operator(3)
    if value == 1:
        if authors.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            print("Desea Buscar un Autor por:\n1. Nombres Completos\n2. Código")
            value2 = validate_operator(2)
            if value2 == 1:
                authors.consult_author_name()
            else:
                authors.consult_author(1)
    elif value == 2:
        if books.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            print("Como Desea Buscar un Libro:\n1. Título\n2. Autor\n3. Código\n4. Secuela de otro Libro")
            print("5. Precuela de otro Libro")
            value2 = validate_operator(5)
            if value2 == 1:
                books.consult_book_name()
            elif value2 == 2:
                books.consult_join()
            elif value2 == 3:
                books.consult_book_id()
            elif value2 == 4:
                if books.check_prequel_or_sequel(1):
                    print("Ingrese el Título del Libro del que quiere buscar Secuelas")
                    name = books.consult_book_name()
                    books.consult_prequel_or_sequel(name, "SECUELA")
                else:
                    print("+"+"-"*35+"+\n"+"|\t\tNo existen Registros\t\t|\n"+"+"+"-"*35+"+")
            else:
                if books.check_prequel_or_sequel(2):
                    print("Ingrese el Título del Libro del que quiere buscar Precuelas")
                    name = books.consult_book_name()
                    books.consult_prequel_or_sequel(name, "PRECUELA")
                else:
                    print("+"+"-"*35+"+\n"+"|\t\tNo existen Registros\t\t|\n"+"+"+"-"*35+"+")
    sleep(3)


def update_info():  # validar la modificacion de autores y libros
    menu_extra("Actualizar")
    cod = None
    value = validate_operator(3)
    value4 = 2
    if value == 1:
        if authors.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            cod = authors.consult_author(3)
            print("Desea actualizar la Información del autor\n1.Actualizar Información completa"
                  "\n2.Actualizar parte de la Información\n3.Volver al Menú")
            value2 = validate_operator(3)
            if value2 == 1:
                print("Se actualizara el Registro del Autor en un orden diferente para mantener la integridad "
                      "del Codigo")
                for i in range(3, 0, -1):
                    authors.modify_author_info(i, cod)
                    save()
            elif value2 == 2:
                print("¿Que Desea Actualizar?\n1.ID del Autor\n2.Nombres Completos del Autor\n3.Fecha "
                      "de Nacimiento del Autor")
                value_2 = validate_operator(3)
                authors.modify_author_info(value_2, cod)
                save()
    if value == 2:
        if books.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            cod_b = books.consult_book_id()
            cod_a = books.consult_update(cod_b)
            print("Desea actualizar la Información del Libro\n1.Actualizar Información completa"
                  "\n2.Actualizar parte de la Información\n3.Volver al Menú")
            value2 = validate_operator(3)
            if not (books.check_register(1)):
                print("Desea Modificar el Libro como una Secuela o Precula de otro Libro\n1.Si\n2.No")
                value4 = validate_operator(2)
                if value4 == 1:
                    print("Ingrese el Código del libro al que se le desea asignar una Secuela o Precuela")
                    cod = books.consult_book_id()
            if value2 == 1:
                print("Se actualizara el Registro del Libro en un orden diferente para mantener la "
                      "integridad del Codigo")
                books.modify_book_info(2, value4, cod_b)
                save()
                books.modify_book_info(3, value4, cod_b, cod_a, cod)
                save()
                books.modify_book_info(4, value4, cod_b)
                save()
                cod2 = books.modify_book_info(1, value4, cod_b)
                save()
                if value4 == 1:
                    title = books.consult_title_book(cod2)
                    title2 = books.consult_title_book(cod)
                    books.enter_prequel_or_sequel(title, title2, cod, cod2)
                    save()
            elif value2 == 2:
                print("¿Que Desea Actualizar?\n1.ID del Libro\n2.Título del Libro\n3.Fecha de Publicación del Libro"
                      "\n4.ID del Autor")
                cont = 0
                value3 = validate_operator(4)
                if value3 == 1:
                    cod2 = books.modify_book_info(value3, value4, cod_b)
                    if value4 == 1:
                        books.modify_book_info(3, value4, cod_b, cod_a, cod)
                        title = books.consult_title_book(cod2)
                        title2 = books.consult_title_book(cod)
                        books.enter_prequel_or_sequel(title, title2, cod, cod2)
                        cont += 1
                elif value3 == 2:
                    books.modify_book_info(value3, value4, cod_b)
                    if value4 == 1:
                        books.modify_book_info(3, value4, cod_b, cod_a, cod)
                elif value3 == 3:
                    books.modify_book_info(value3, value4, cod_b, cod_a, cod)
                else:
                    books.modify_book_info(value3, value4, cod_b)
                    if value4 == 1:
                        books.modify_book_info(3, value4, cod_b, cod_a, cod)
                if value4 == 1:
                    if cont == 0:
                        title = books.consult_title_book(cod_b)
                        title2 = books.consult_title_book(cod)
                        books.enter_prequel_or_sequel(title, title2, cod, cod_b)
                save()


def save():  # pequeño recordatorio para cada vez que actualices un dato
    print("Guardando")
    sleep(2)
    print("Registros guardados correctamente")
    sleep(1)


def delete():  # validar la eliminacion de autores y libros,
    menu_extra("Eliminar")
    value = validate_operator(3)
    if value == 1:
        if authors.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            if authors.delete_author():
                save()
    elif value == 2:
        if books.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            if books.delete_book():
                save()


def review():  # revisar informacion completa de autores y libros
    menu_extra("Revisar")
    value = validate_operator(3)
    if value == 1:
        if authors.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            authors.list_all()
    elif value == 2:
        if books.check_register():
            print("+" + "-" * 35 + "+\n" + "|\t\tNo existen Registros\t\t|\n" + "+" + "-" * 35 + "+")
        else:
            books.list_all()


def close_progam():  # cerrar programa
    print("+" + "-" * 31 + "+\n" + "|\t\t\tSaliendo\t\t\t|" + "\n+" + "-" * 31 + "+")
    sleep(2)
    exit()


if __name__ == "__main__":
    authors = Authors(None, None, None, None)
    books = Books(None, None, None, None)
    while True:
        operation = menu()
        while True:
            if operation == 1:
                create()
                break
            elif operation == 2:
                search()
                break
            elif operation == 3:
                update_info()
                break
            elif operation == 4:
                delete()
                break
            elif operation == 5:
                review()
                break
            else:
                close_progam()
        print("+"+"-"*31+"+\n"+"|\t\tVolviendo al menú\t\t|"+"\n+"+"-"*31+"+")
        sleep(2)
