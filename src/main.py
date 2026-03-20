from flask import Flask, render_template, request, redirect
import mysql.connector

# CONECTAR AO BANCO DE DADOS.
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Luiz/30/09",
        database="db_users"
    )

app = Flask(__name__)

# TELA INICIAL (LOGIN)
@app.route("/")
def home():
    return render_template("login.html")

# SALVAR OS DADOS CRIADOS PELO CLIENTE, SALVA NO BANCO DE DADOS.

@app.route("/register_user", methods=["POST"])
def register_user():
    
    user_name = request.form.get("name")
    user_email = request.form.get("email")

    connection = connect_db()
    cursor = connection.cursor()

    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (user_name, user_email)

    cursor.execute(query, values)

    connection.commit()
    connection.close()
    return f"Usuário Salvo com Sucesso!"

# MOSTRA A LISTA DOS USUARIOS CRIADOS.

@app.route("/list_users")
def list_users():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email FROM users")

    users = cursor.fetchall()

    connection.close()

    return render_template("list_users.html", users = users)

# BOTÃO DE EXCLUIR O USUARIO DA TABELA

@app.route("/delete_user/<int:id>", methods =["POST"])
def delete_user(id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (id,))

    connection.commit()
    connection.close()

    return redirect("/list_users")

# BOTÃO PARA EDITAR CADASTRO DO USUARIO

@app.route("/edit_user/<int:id>")
def edit_user(id):
    connection = connect_db()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    users = cursor.fetchone()

    return render_template("edit_users.html", users = users)

# BOTÃO PARA SALVAR A EDIÇÃO DO USUARIO

@app.route("/update_user", methods=["POST"])
def update_user():

    id = request.form.get("id")
    user_name = request.form.get("name")
    user_email = request.form.get("email")

    connection = connect_db()
    cursor = connection.cursor()

    query = "UPDATE users SET name= %s, email= %s WHERE id= %s"
    values = (user_name, user_email, id)

    cursor.execute(query, values)

    connection.commit()
    connection.close()
    return redirect("/list_users")

app.run(debug=True)