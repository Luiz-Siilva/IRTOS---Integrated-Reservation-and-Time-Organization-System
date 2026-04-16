from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
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
app.secret_key = "segredo"

# TELA INICIAL (LOGIN)
@app.route("/")
def home():
    return render_template("login.html")

# TELA DE CRIAR USUARIO
@app.route("/create_users")
def create_users():
    return render_template("create_users.html")

# SALVAR OS DADOS CRIADOS PELO CLIENTE, SALVA NO BANCO DE DADOS.
@app.route("/register_user", methods=["POST"])
def register_user():
    
    user_name = request.form.get("name")
    user_email = request.form.get("email")
    user_phone = request.form.get("phone")
    user_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    #BLOQUEAR CAMPOS SEM NADA
    if not user_name or not user_email or not user_phone or not user_password or not confirm_password:
        flash("Preencha todos os campos")
        return redirect("/register_user")

    #VALIDAR SENHA
    if user_password != confirm_password:
        flash("As senhas não coincidem")
        return render_template("/create_users.html",
                               name=user_name,
                               email=user_email,
                               phone=user_phone)

    connection = connect_db()
    cursor = connection.cursor()

    #VERIFICAR SE EMAIL JÁ EXISTE
    cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()

    if user:
        flash("Esse email já está cadastrado!")
        connection.close()
        return redirect("/")

    #CRIPTOGRAFAR SENHA
    password_hash = generate_password_hash(user_password)

    query = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)"
    values = (user_name, user_email, user_phone, password_hash)

    cursor.execute(query, values)

    connection.commit()
    connection.close()

    flash("Usuário cadastrado com sucesso!")

    return redirect("/")

# LOGIN DENTRO DO SISTEMA

@app.route("/login_user", methods=["POST"])
def login_user():

    user_email = request.form.get("email")
    user_password = request.form.get("password")

    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    #BUSCAR USUARIO PELO EMAIL
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (user_email,))
    user = cursor.fetchone()

    connection.close()

    #SE NÃO ENCONTROU O USUARIO
    if user is None:
        flash("Email ou senha inválidos!")
        return redirect("/")
    
    #VERIFICAR SENHA
    if check_password_hash(user["Password"], user_password):
        #LOGIN CORRETO
        session["user_id"] = user["Id_users"]
        session["user_name"] = user["Name"]

        return render_template("system_agend.html")
    else:
        #SENHA INVALIDA
        flash("Email ou senha inválida!")
        return redirect("/")

app.run(debug=True)


