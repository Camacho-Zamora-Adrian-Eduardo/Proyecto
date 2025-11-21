from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'contraseña_muy_segura123'


USUARIOS_REGISTRADOS = {"admin@cetis.edu.mx": {"nombre": "Admin", "password": "Cetis61"}}


@app.route("/")
def index():
    return render_template("iniciosesion.html")


@app.route('/validaSesion', methods=['POST'])
def validasesion():

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Por favor ingresa email y contraseña', 'error')
        return render_template('iniciosesion.html')

    if email in USUARIOS_REGISTRADOS:
        usuario = USUARIOS_REGISTRADOS[email]

        if usuario['password'] == password:
            session['usuario_email'] = email
            session['usuario'] = usuario['nombre']
            session['logueado'] = True
            return redirect(url_for('interfaz'))
        else:
            flash('Contraseña incorrecta', 'error')
            return render_template('iniciosesion.html')
    else:
        flash('Usuario no encontrado', 'error')
        return render_template('iniciosesion.html')



@app.route("/interfaz")
def interfaz():
    return render_template("interfazinicio.html")


@app.route("/analisisdecomida")
def analisis():
    return render_template("analisis.html")


@app.route("/calculadoraGET")
def calculadoraGET():
    return render_template("calculadoraGET.html")


@app.route("/calcularGET", methods=["POST"])
def calcular_GET():

    try:
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = int(request.form["edad"])
        genero = request.form["genero"]
        actividad = request.form["actividad"]

        if genero == 'hombre':
            tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
        else:
            tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

        factores = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "intenso": 1.725,
            "muy_intenso": 1.9
        }

        get = tmb * factores[actividad]

    except Exception:
        flash("Datos inválidos. Revisa tu información.", "error")
        return redirect(url_for("calculadoraGET"))

    return render_template(
        "calculadoraGET.html",
        get=get,
        peso=peso,
        altura=altura,
        edad=edad,
        genero=genero,
        actividad=actividad
    )



@app.route("/calculadoraIMC")
def calculadoraIMC():
    return render_template("calculadoraIMC.html")

@app.route("/calcularIMC", methods=["POST"])
def calcular_IMC():
    try:
        peso = float(request.form["peso"])
        altura = float(request.form["altura"]) / 100  

        imc = peso / (altura * altura)

        return render_template("calculadoraIMC.html", imc=round(imc, 2))

    except:
        flash("Datos inválidos", "error")
        return redirect(url_for("calculadoraIMC"))


@app.route("/calculadoraMACRO")
def calculadoraMACRO():
    return render_template("calculadoraMACRO.html")

@app.route("/macroscalculados", methods=['POST'])
def macroscalculados():

    try:
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])
        genero = request.form['genero']
        actividad = request.form['actividad']
        objetivo = request.form['objetivo']
        
        if objetivo == "mantener":
            calorias = 0
        else:
            calorias = int(request.form['calorias'])

    except Exception:
        flash("Datos inválidos. Revisa tu información.", "error")
        return redirect(url_for("calculadoraMACRO"))

    tdee, proteinas, carbohidratos, grasas = calcular_macros(
        peso, altura, edad, genero, actividad, objetivo, calorias
    )

    return render_template(
        "calculadoraMACRO.html",
        tdee=tdee,
        proteinas=proteinas,
        carbohidratos=carbohidratos,
        grasas=grasas,
        peso=peso,
        altura=altura,
        edad=edad,
        genero=genero,
        actividad=actividad,
        objetivo=objetivo,
        calorias=calorias
    )


def calcular_macros(peso, altura, edad, genero, actividad, objetivo, calorias):

    if genero == 'hombre':
        bmr = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    else:
        bmr = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

    factores = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "intenso": 1.725
    }

    tdee = bmr * factores.get(actividad, 1.2)

    if objetivo == 'perder':
        tdee -= calorias
    elif objetivo == 'ganar':
        tdee += calorias

    proteinas = (0.25 * tdee) / 4
    carbohidratos = (0.50 * tdee) / 4
    grasas = (0.25 * tdee) / 9

    return round(tdee, 2), round(proteinas, 2), round(carbohidratos, 2), round(grasas, 2)


@app.route("/calculadoraPCI")
def calculadoraPI():
    return render_template("calculadoraPCI.html")

@app.route("/calcularPCI", methods=["POST"])
def calcular_PCI():
    try:
        altura = float(request.form["altura"])
        genero = request.form["genero"]

        altura_pulg = altura / 2.54

        if genero == "hombre":
            pci = 50 + 2.3 * (altura_pulg - 60)
        else:
            pci = 45.5 + 2.3 * (altura_pulg - 60)

        return render_template("calculadoraPCI.html", pci=round(pci, 2))

    except:
        flash("Datos inválidos", "error")
        return redirect(url_for("calculadoraPCI"))


@app.route("/calculadoraTMB")
def calculadoraTMB():
    return render_template("calculadoraTMB.html")

@app.route("/calcularTMB", methods=["POST"])
def calcular_TMB_route():
    try:
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = int(request.form["edad"])
        genero = request.form["genero"]

        if genero == "hombre":
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        return render_template("calculadoraTMB.html", tmb=round(tmb, 2))

    except:
        flash("Datos inválidos", "error")
        return redirect(url_for("calculadoraTMB"))








@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route('/registrame', methods=['POST'])
def registrame():

    nombre = request.form.get("nombreCompleto")
    correo = request.form.get("correo")
    password = request.form.get("contraseña")

    if not nombre or not correo or not password:
        flash("Todos los campos son obligatorios", "error")
        return render_template("registro.html")

    flash(f"Tu cuenta ha sido creada, {nombre}")
    return redirect(url_for("index"))

@app.route("/recetas")
def recetas():
    return render_template("recetassaludables.html")


if __name__ == "__main__":
    app.run(debug=True)
