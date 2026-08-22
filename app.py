from flask import Flask, render_template, request, redirect, flash #Flash é utilizado para dar alertas ao usuário na tela
import mysql.connector
import werkzeug.security as security # Biblioteca que será utilizada para criptografar a senha do usuário

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

@app.route("/cadastro_usuario", methods="POST")
def cadastroUser():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    confirmar_senha = request.form.get("confirm-senha")

    if senha != confirmar_senha:
        flash()
        return redirect('/cadastro_usuario')

    senha_criptografada = security.generate_password_hash(senha)
    try:

        conexao = mysql.connector.connect(**bd_config)
        cursor = conexao.cursor(dictionary=True)

        cursor.close()
        conexao.close()
    except:
        pass
    finally:
        pass
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