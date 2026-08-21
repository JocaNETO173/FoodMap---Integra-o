from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

bd_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'escola',
    'database': 'foodmap',
    'ssl_disabled': True
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro_usuario")
def cadastroUser():
    return render_template("cadastro.html")

@app.route("/restaurantes", methods=["GET", "POST"])
def restaurantes():
    restaurantes = []
    termo = request.form.get("termo", "")  # Pega o que o usuário digitou

    conexao = mysql.connector.connect(**bd_config)
    # Retorna os resultados como dicionários
    cursor = conexao.cursor(dictionary=True)

    if termo:
        query = "SELECT * FROM restaurantes WHERE nome LIKE %s"
        cursor.execute(query, (f"%{termo}%",))
    else:
        # Se não houver busca, exibe todos (ou deixe vazio se preferir)
        cursor.execute("SELECT * FROM restaurantes")

    restaurantes = cursor.fetchall()

    cursor.close()
    conexao.close()
    return render_template("restaurantes_user.html", restaurantes=restaurantes, termo=termo)
    # if (usuario == user):
    #     
    # elif (usuario == admin):
    #     return render_template("restaurantes_admin.html", restaurantes=restaurantes, termo=termo)

if __name__ == "__main__":
    app.run(debug=True)