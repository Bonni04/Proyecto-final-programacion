from flask import Flask, request, g, redirect, url_for, render_template, flash, session
app = Flask(__name__)


lista = []
usuarioss = []

##################################################################

##Esta parte consiste en el login de la pagina primero nos trae el template desde html de nombre login y
##luego nos pide usuario y demas datos si son correctos son redireccionados a la pagina principal llamada
##Vuelos en caso que no se encuentre esta persona es redireccionada a la pagina registro
@app.route("/")
def pagLogin():                                                                                             
    return(render_template('login.html'))

@app.route("/ingresar",methods = ["GET","POST"])                                                            
def ingresar():

    global lista
    global usuarios

    usuario= request.form["Usuario"]
    contrasena = request.form["Contraseña"]
    correo = request.form["Correo"]
    telefono = request.form["Telefono"]

    archivo =open("basededatos.txt",mode = 'r')
    for dato in archivo:
        j = dato.split()
        if (j[0]== usuario and j[1] == contrasena and j[2] == correo and j[3] == telefono):
                usuarioss.append(usuario)
                archivo.close()
                return redirect(url_for('vuelos'))                  
    archivo.close()
    return redirect(url_for('pagRegistro'))




#########################################################################

##Este apartado consiste en tres funciones la primera leerArchivo nos permite  leer vuelos que hay en el txt
##Luego existe la funcion vuelos e imprimir vuelos la cual en esta se encuentra las casillas para que una persona
##pueda buscar el vuelo tambien para que pueda ingresar a su perfil y poder reservar el vuelos este es como la parte
##principal de la pagina

def leerArchivo():
    """
    """
    archivo = open ("datosvuelos.txt",mode = "r")
    
    for i in range(14):
        archivo.readline()
        
    aeropuertos = []
    for i in range(15,37):
        linea = archivo.readline()
        aeropuertos.append(linea)
        
    for i in range(38,61):
        archivo.readline()
        
    vuelos = []
    for i in range(62,500):
        linea = archivo.readline()
        vuelos.append(linea)

    archivo.close()

    return vuelos




@app.route ("/Pagina principal")
def vuelos():
    """
    """
    entries = {}

    return render_template("vuelos.html",entries = entries)




@app.route("/Lista de vuelos",methods = ["GET","POST"])
def imprimirVuelos():
    """
    """
    vuelos = leerArchivo()
    entries = {"vuelos":[]}
    
    if(request.method == 'POST'):
        if(request.form['boton'] == 'Reservar vuelo'):
             return redirect(url_for('reserva'))
    if(request.method == 'POST'):
        if(request.form['boton'] == 'Mi perfil'):
             return redirect(url_for('pagusuarios'))
    
    if(request.method == 'POST'):
        if(request.form['boton'] == 'Sin Preferencia'):        
                origen = request.form['origen']
                llegada = request.form ['llegada']
                for linea in vuelos:
                    tmp = linea.split()
                    if (tmp[2] == origen and tmp [4] == llegada):
                        entries ["vuelos"].append(linea)
                entries ["numero"] = len(entries["vuelos"])                    
                return render_template("imprimir1.html", entries = entries)

        if(request.form['boton'] == '1 Preferencia'):
                origen = request.form['origen']
                llegada = request.form ['llegada']
                preferencia1 = request.form ['preferencia1']
                for linea in vuelos:
                    tmp = linea.split()
                    if (tmp[2] == origen and tmp [4] == llegada and tmp [6] == preferencia1):
                        entries ["vuelos"].append(linea)
                        
                entries ["numero"] = len(entries["vuelos"])                    
                return render_template("imprimir1.html", entries = entries)
            
        if(request.form['boton'] == '2 Preferencias'):
                origen = request.form['origen']
                llegada = request.form ['llegada']
                preferencia2 = request.form ['preferencia2']
                for linea in vuelos:
                    tmp = linea.split()
                    if (tmp[2] == origen and tmp [4] == llegada and tmp [6] == preferencia2):
                        entries ["vuelos"].append(linea)
                        
                entries ["numero"] = len(entries["vuelos"])                    
                return render_template("imprimir1.html", entries = entries)


                    
########################################################################
            
##Este apartado es muy similar al anterior la primera funcion nos permite leer un txt en donde estan los vuelos
##reservados de cada persona luego en la funcion usuario esta nos permite que la persona ingrese tres datos que son
##usuarios correo  y telefono si estos son correctos se muestran todas las reservas que ha hecho esta persona

def leerArchivoUsuario():
    """
    """
    
    archivo = open ("vuelosReservados.txt",mode = "r")

    usuarios = []
    for i in range(2): ####IMPORTANTE ESTE 2 TIENE QUE SER CAMBIADO MANUALMENTE CUANDO CADA PERSONA HAGA UNA RESERVA
    
        linea = archivo.readline()
        usuarios.append(linea)   
        
    archivo.close()
    
    return usuarios



@app.route ("/Mi perfil")
def pagusuarios():
    """
    """
    entries = {}

    return render_template("usuarios.html",entries = entries)




@app.route("/Historial",methods = ["GET","POST"])
def usuarios():
    """
    """
    usuarios = leerArchivoUsuario()
    entries = {"usuarios":[]}
    global usuarioss

    if (request.method == "POST"):
        usuario = request.form['usuario']
        correo = request.form['correo']
        telefono = request.form['telefono']

        if usuario in usuarioss:
            for linea in usuarios:
                    tmp = linea.split()
                    if (tmp[0] == usuario and tmp[1] == correo and tmp[2] == telefono ):
                        entries ["usuarios"].append(linea)

            entries ["numero"] = len(entries["usuarios"])
            return render_template("historialUsuarios.html", entries = entries)
        else:
            return render_template("policia.html", entries = entries)
            



########################################################################################

##Este apartado nos permite hacer las reservas de cada usuario esta  nos pediria ciertos datos de la aerolinea que
##va a tomar  esta persona al igual su usuario contrasena entre otros  estos seran guardados en un txt llamada
##vuelos reservados

@app.route("/reservas")
def reserva():
    """
    """
    entries = {}
    
    return(render_template('reserva.html', entries = entries))


@app.route("/Reserva de vuelos",methods = ["GET","POST"])
def reservarVuelos():
    """
    """
    entries = {}

    
    a = request.form["Aerolinea"]
    b = request.form["Numero Vuelo"]
    c = request.form["Ciudad 1"]
    d = request.form["Ciudad 2"]
    e = request.form["Usuario"]
    f = request.form["Contrasena"]
    g = request.form["Correo"]
    i = request.form["Telefono"]

    archivo = open("datosvuelos2.txt", mode = 'r')
    for dato in archivo :
        h = dato.split()
        if (h[0]== a and h[1]== b and h[2] == c and h[4] == d) :

                
                archivo = open ("vuelosReservados.txt",mode = "a")            
                archivo.write(e +' ')
                archivo.write(g +' ')
                archivo.write(i +' ')
                archivo.write(h[0]+' ')
                archivo.write(h[1]+' ')
                archivo.write(h[2]+' ')
                archivo.write(h[3]+' ')
                archivo.write(h[4]+' ')
                archivo.write(h[5]+' ')
                archivo.write(h[6]+'\n')
                archivo.close
               

                return(render_template('reserva.html'))



        if(request.method == 'POST'):
            if(request.form['boton'] == 'Volver al menu'):
                 return redirect(url_for('vuelos'))


#########################################################################################

##Este apartado el cual es el ultimo consiste  en registrarse en nuestra pagina en este se pediran 4 datos
##Los cuales son usuario contrasena correo y telefono estos seran guardados en un txt llamado basededatos.txt
##despues del registro sera redireccionado a la pagina del login 
        


@app.route("/reg")
def pagRegistro():
    return(render_template('registro.html'))



@app.route("/registrarse",methods = ["GET","POST"])
def registrarse():
    global lista
    usuario= request.form["Usuario"]
    contrasena = request.form ["Contraseña"]
    correo = request.form["Correo"]
    telefono = request.form["Telefono"]

  
    archivo = open ("basededatos.txt",mode = "a")
    archivo.write(usuario+' ')
    archivo.write(contrasena+' ')
    archivo.write(correo+' ')
    archivo.write(telefono+ '\n')

    archivo.close()
    lista.append(usuario)
    lista.append(contrasena)
    lista.append(correo)
    lista.append(telefono)



    return redirect(url_for("pagLogin",lista = lista))








app.run(debug = True)
