from flask import Flask, render_template, request, redirect
import mysql.connector

# CONECTAR AO BANCO DE DADOS.
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Luiz/30/09",
        database="db_teste"
    )

app = Flask(__name__)

# TELA INICIAL (LOGIN)
@app.route("/")
def home():
    return render_template("login.html")

# SALVAR OS DADOS CRIADOS PELO CLIENTE, SALVA NO BANCO DE DADOS.

@app.route("/cadastrar_usuario", methods=["POST"])
def cadastrar_usuarios():
    
    nome = request.form.get("nome")
    email = request.form.get("email")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO pessoas (nome, email) VALUES (%s, %s)"
    valores = (nome, email)

    cursor.execute(sql, valores)

    conexao.commit()
    conexao.close()
    return f"Usuário Salvo com Sucesso!"

# MOSTRA A LISTA DOS USUARIOS CRIADOS.

@app.route("/lista_de_pessoas")
def lista_de_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, email FROM pessoas")

    pessoas = cursor.fetchall()

    conexao.close()

    return render_template("usuarios.html", pessoas = pessoas)

# BOTÃO DE EXCLUIR O USUARIO DA TABELA

@app.route("/deletar_cadastro/<int:id>", methods =["POST"])
def deletar_usuario(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM pessoas WHERE id = %s", (id,))

    conexao.commit()
    conexao.close()

    return redirect("/lista_de_pessoas")

# BOTÃO PARA EDITAR CADASTRO DO USUARIO

@app.route("/editar_cadastro/<int:id>")
def editar_cadastro(id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM pessoas WHERE id = %s"
    cursor.execute(sql, (id,))
    pessoas = cursor.fetchone()

    return render_template("editar.html", pessoas = pessoas)

# BOTÃO PARA SALVAR A EDIÇÃO DO USUARIO

@app.route("/atualizar_cadastro", methods=["POST"])
def atualizar_cadastro():

    id = request.form.get("id")
    nome = request.form.get("nome")
    email = request.form.get("email")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE pessoas SET nome= %s, email= %s WHERE id= %s"
    valores = (nome, email, id)

    cursor.execute(sql, valores)

    conexao.commit()
    conexao.close()
    return redirect("/lista_de_pessoas")

app.run(debug=True)