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

@app.route("/calculadora")
def calculadora():
    return render_template("calculadora.html")

@app.route("/calcular")
def calcular():
    error=None
    
    return render_template("calculadora.html")

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