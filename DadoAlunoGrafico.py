from flask import Flask, request, render_template_string, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["meu_banco_de_dados"]
colecao = db["minha_colecao_dados_grafico"]

@app.route('/')
def form():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
           <title>Registro de Alunos</title>
    </head>
    <body>
        <h2>Formulário de Registro de Alunos</h2>
        <form action="/save" method="post">
            <label for="nome">Nome:</label><br>
            <input type="text" id="nome" name="nome"><br>
            <label for="idade">Idade:</label><br>
            <input type="number" id="idade" name="idade"><br>
            <label for="altura">Altura (em metros):</label><br>
            <input type="number" step="0.01" id="altura" name="altura"><br>
            <label for="peso">Peso (em kg):</label><br>
            <input type="number" step="0.01" id="peso" name="peso"><br>
            <label for="imc">IMC:</label><br>
            <input type="number" step="0.01" id="imc" name="imc" readonly><br>
            <input type="submit" value="Registrar">
        </form>
        <script>
            document.getElementById('altura').addEventListener('input', calculateIMC);
            document.getElementById('peso').addEventListener('input', calculateIMC);

            function calculateIMC() {
                const altura = parseFloat(document.getElementById('altura').value);
                const peso = parseFloat(document.getElementById('peso').value);
                if (!isNaN(altura) && !isNaN(peso)) {
                    const imc = peso / (altura * altura);
                    document.getElementById('imc').value = imc.toFixed(2);
                }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()
    resultado = colecao.insert_one(data)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Salvo</title>
    </head>
    <body>
        <h2>Dados inseridos com o ID: {{resultado.inserted_id}}</h2>
        <button onclick="window.location.href='/'">Voltar</button>
    </body>
    </html>
    ''', resultado=resultado)

if __name__ == '__main__':
    app.run()