from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisisdecomida")
def analisis():
    return render_template("analisis.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route('/registrame', methods= ("GET", "POST"))
def registro():
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









if __name__ == "__main__":
    app.run(debug=True)