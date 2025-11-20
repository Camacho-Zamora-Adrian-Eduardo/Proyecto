from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'contraseña_muy_segura123'

USUARIOS_REGISTRADOS = {
    "admin@cetis.edu.mx": {"nombre": "Admin", "password": "Cetis61"}}


@app.route("/")
def index():
    return render_template("iniciosesion.html")

@app.route('/validaSesion', methods=['GET','POST'])
def validasesion():
    
    if request.method == "POST":
        email = request.form.get('email','').strip()
        password = request.form.get('password','')
        # Validad credenciales
        if not email or not password:
            flash('Por favor ingresa email y contraseña','error')
        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]
            if usuario['password'] == password:
                # Credenciales correctas
                session['usuario_email'] = email
                session['usuario'] = usuario['nombre']
                session['logueado'] = True
                
                return render_template('calculadora.html')
            else:
                flash('Contraseña incorrecta','error')
        else:
            flash('Usuario no encontrado','error')
            
            return render_template('iniciosesion.html')

@app.route("/analisisdecomida")
def analisis():
    return render_template("analisis.html")

@app.route("/calculadoraGET")
def calculadoraGET():
    return render_template("calculadoraGET.html")

@app.route("/calculadoraIMC")
def calculadoraIMC():
    return render_template("calculadoraIMC.html")



@app.route("/calculadoraMACRO", methods=['GET', 'POST'])
def calculadoraMACRO():
    return render_template("calculadoraMACRO.html")

@app.route("/macroscalculados")
def macroscalculados():
    
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])
        genero = request.form['genero']
        actividad = request.form['actividad']
        objetivo = request.form['objetivo']
        calorias = int(request.form['calorias'])

        tdee, proteinas, carbohidratos, grasas = calcular_macros(
            peso, altura, edad, genero, actividad, objetivo, calorias)

        return render_template('calculadoraMACRO.html', tdee=tdee, proteinas=proteinas,
                                carbohidratos=carbohidratos, grasas=grasas,
                                peso=peso, altura=altura, edad=edad,
                                genero=genero, actividad=actividad,
                                objetivo=objetivo, calorias=calorias)


def calcular_macros(peso, altura, edad, genero, actividad, objetivo, calorias):
    if genero == 'hombre':
        bmr = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    else:
        bmr = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    
    if actividad == 'sedentario':
        tdee = bmr * 1.2
    elif actividad == 'ligero':
        tdee = bmr * 1.375
    elif actividad == 'moderado':
        tdee = bmr * 1.55
    elif actividad == 'intenso':
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9

    if objetivo == 'perder':
        tdee -= calorias  
    elif objetivo == 'ganar':
        tdee += calorias  


    proteinas = 0.2 * tdee / 4  
    carbohidratos = 0.5 * tdee / 4  
    grasas = 0.3 * tdee / 9  

    return tdee, proteinas, carbohidratos, grasas



@app.route("/calculadoraPI")
def calculadoraPI():
    return render_template("calculadoraPI.html")

@app.route("/calculadoraTMB")
def calculadoraTMB():
    return render_template("calculadoraTMB.html")
    


@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route('/registrame', methods= ("GET", "POST"))
def registrame():
    error = None
    if request.method == "POST":
        nombreCompleto = request.form["nombreCompleto"]
        fecha = request.form["fecha"]
        correo = request.form["correo"]
        password = request.form["contraseña"]
        
    if error != None:
        flash(error)
        return render_template("crear.html")
    else:
        flash(f"Tu cuenta se a creado {nombreCompleto}")
        return render_template("inicio.html")
    
@app.route("/interfaz")
def interfaz():
    return render_template("interfazinicio.html")









if __name__ == "__main__":
    app.run(debug=True)