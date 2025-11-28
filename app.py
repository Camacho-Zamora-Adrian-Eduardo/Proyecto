from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from deep_translator import GoogleTranslator


app = Flask(__name__)
app.config ['SECRET_KEY'] = '20_cosas_que_no_sabias_de_las_empanadas'


Usuarios_registrados = {"admin@cetis.edu.mx": {"nombre": "Admin", "password": "Cetis61"}}

Nutrientes_importantes = {
    "Energy",
    "Protein",
    "Total lipid (fat)",
    "Carbohydrate, by difference",
    "Fiber, total dietary",
    "Sugars, total including NLEA",
    "Calcium, Ca",
    "Iron, Fe",
    "Sodium, Na",
    "Potassium, K",
    "Vitamin C, total ascorbic acid",
    "Vitamin A, RAE"
}
Traducciones = {
    "Energy": "Energía (kcal)",
    "Protein": "Proteína",
    "Total lipid (fat)": "Grasa total",
    "Carbohydrate, by difference": "Carbohidratos",
    "Fiber, total dietary": "Fibra dietética",
    "Sugars, total including NLEA": "Azúcares totales",
    "Calcium, Ca": "Calcio",
    "Iron, Fe": "Hierro",
    "Sodium, Na": "Sodio",
    "Potassium, K": "Potasio",
    "Vitamin C, total ascorbic acid": "Vitamina C",
    "Vitamin A, RAE": "Vitamina A",

}

api_key = "b48he0KjRd6oDnYooKxLr1OCO9pCoJPuX1bqmvDu"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"



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

    if email in Usuarios_registrados:
        usuario = Usuarios_registrados[email]

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



@app.route("/panel")
def panel():
    return render_template("panelControl.html")

@app.route("/recomendaciones", methods=["POST"])
def recomendaciones():

    sueno = int(request.form.get("sueno", 0))
    comidas = int(request.form.get("comidas", 0))
    deporte = request.form.get("deporte", "")
    actividad = request.form.get("actividad", "")
    cereales = int(request.form.get("cereales", 0))
    proteinas = int(request.form.get("proteinas", 0))
    grasas = int(request.form.get("grasas", 0))
    frutas = int(request.form.get("frutas", 0))
    verduras = int(request.form.get("vegetales", 0))
    leche = int(request.form.get("leche", 0))
    azucar = int(request.form.get("azucar", 0))
    leguminosas = int(request.form.get("leguminosas", 0))
    agua = float(request.form.get("agua", 0))

    recomendaciones = []


    if sueno < 7:
        recomendaciones.append("*Duerme más de 7 horas al día para mejorar tu rendimiento.*")
    else:
        recomendaciones.append(" Buen trabajo con tus horas de sueño.")

    if comidas < 3:
        recomendaciones.append("*Haz al menos 3 comidas al día para mantener tu energía estable.*")
    else:
        recomendaciones.append(" Tu frecuencia de comidas es adecuada.")

    if actividad == "baja":
        recomendaciones.append(" *Aumenta tu actividad física al menos 30 min diarios.*")
    elif actividad == "media":
        recomendaciones.append(" Buen nivel de actividad física, sigue así.")
    else:
        recomendaciones.append(" Excelente nivel de actividad física.")

    
    rec = {
        "cereales": 6,
        "proteinas": 5,
        "grasas": 3,
        "frutas": 2,
        "verduras": 3,
        "leche": 1,
        "azucar": 50,
        "leguminosas": 1,
        "agua": 8
    }

    def revisar_consumo(nombre, valor_actual, valor_recomendado, bueno, bajo, alto):
        if valor_actual < valor_recomendado:
            recomendaciones.append(bajo)
        elif valor_actual > valor_recomendado:
            recomendaciones.append(alto)
        else:
            recomendaciones.append(bueno)

    revisar_consumo("cereales", cereales, rec["cereales"],
        " Buen consumo de cereales.",
        " *Te faltan cereales integrales en tu alimentación.*",
        " *Estás consumiendo demasiados cereales, reduce un poco.*"
    )

    revisar_consumo("proteinas", proteinas, rec["proteinas"],
        " Buen consumo de proteínas.",
        " *Incluye más proteínas magras como pollo, pescado, huevo.*",
        " *Reduce tu exceso de proteínas.*"
    )

    revisar_consumo("frutas", frutas, rec["frutas"],
        " Buen consumo de frutas.",
        " *Consume más frutas frescas.*",
        " *Demasiada fruta puede aumentar el azúcar natural.*"
    )

    revisar_consumo("verduras", verduras, rec["verduras"],
        " Buen consumo de verduras.",
        " *Necesitas más verduras.*",
        " *Estás consumiendo demasiadas verduras (raro, pero posible).*"
    )

    revisar_consumo("leche", leche, rec["leche"],
        " Buen consumo de lácteos.",
        " *Incluye una porción de leche o derivados.*",
        " *Estás consumiendo demasiados lácteos.*"
    )

    revisar_consumo("azúcar", azucar, rec["azucar"],
        " Buen control de azúcar.",
        " Tu consumo de azúcar es bajo.",
        " *Reduce urgentemente tus niveles de azúcar.*"
    )

    revisar_consumo("leguminosas", leguminosas, rec["leguminosas"],
        " Buen consumo de leguminosas.",
        " *Incluye más frijoles, lentejas o garbanzos en tu dieta.*",
        " *Consumo excesivo de leguminosas.*"
    )

    revisar_consumo("agua", agua, rec["agua"],
        " Excelente hidratación.",
        " *Te falta beber más agua, mínimo 2 litros diarios.*",
        " *Estás tomando demasiada agua.*"
    )

    return render_template("panelControl.html", recomendaciones=recomendaciones)



@app.route("/analisisdecomida")
def analisis():
    return render_template("analisis.html")

def traducir(texto):
    return GoogleTranslator(source='es', target='en').translate(texto)

@app.route('/search', methods=['POST'])
def search_alimento():
    alimento_name = request.form.get('alimento_name', '').strip().lower()

    if not alimento_name:
        flash("Por favor, ingrese un alimento", "danger")
        return redirect(url_for('analisis'))

    alimento_traducido = traducir(alimento_name)

    headers = {"X-Api-Key": api_key}
    params = {"query": alimento_traducido}

    try:
        respuesta = requests.get(API_URL, headers=headers, params=params)
        respuesta.raise_for_status()
        data = respuesta.json()

        if 'foods' not in data or len(data['foods']) == 0:
            flash(f'Alimento \"{alimento_name}\" no encontrado', 'danger')
            return redirect(url_for('analisis'))

        alimento_data = data['foods'][0]

        alimento_info = {
            "name": alimento_data.get("description", "").title(),
            "fdcId": alimento_data.get("fdcId"),
            "foodCategory": Traducciones.get(
                alimento_data.get("foodCategory", "Desconocida"),
                alimento_data.get("foodCategory", "Desconocida")
            ),
            "dataSource": Traducciones.get(
                alimento_data.get("dataSource", "Desconocido"),
                alimento_data.get("dataSource", "Desconocido")
            ),
            "brandOwner": alimento_data.get("brandOwner", "Desconocido"),

            "foodNutrients": [
                {
                    "name": Traducciones.get(
                        nutrient.get("nutrientName", "Desconocido"),
                        nutrient.get("nutrientName", "Desconocido")
                    ),
                    "value": nutrient.get("value", 0),
                    "unit": nutrient.get("unitName", "")
                }
                for nutrient in alimento_data.get("foodNutrients", [])
                if nutrient.get("nutrientName") in Nutrientes_importantes
            ]
        }

        return render_template("alimento.html", alimento=alimento_info)

    except requests.exceptions.RequestException as e:
        flash(f"Error al hacer la solicitud: {e}", "danger")
        return redirect(url_for('analisis'))



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


@app.route("/creacuenta")
def crearcuenta():
    return render_template("crearcuenta.html")


@app.route('/registrame', methods=['POST'])
def registrame():

    
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellidos")
    email = request.form.get("email")
    password = request.form.get("pasword")
    
    if not nombre or not email or not password:
        flash("Todos los campos son obligatorios", "error")  
        return render_template("crearcuenta.html")

    Usuarios_registrados[email] = {
        "nombre": nombre,
        "password": password
        }
    

    flash(f"Tu cuenta ha sido creada, {nombre}")
    return redirect("/interfaz")

@app.route("/recetas")
def recetas():
    return render_template("recetassaludables.html")

@app.route("/interfaz")
def interfaz():
    return render_template("interfazinicio.html")

@app.route("/educacion")
def educacion():
    return render_template("Educacion.html")


if __name__ == "__main__":
    app.run(debug=True)
