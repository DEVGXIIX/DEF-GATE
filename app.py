# Bibliotecas usadas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, request, make_response
import pandas as pd

# Inicializa o SDK do Firebase com as credenciais baixadas
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

# Cria uma conexão com o Firestore
db = firestore.client()

app = Flask(__name__)

# Define a rota para cadastrar um aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    # Obtém os dados do aluno a partir do corpo da requisição
    aluno = request.json
    # Adiciona o aluno ao Firestore
    db.collection('alunos').add(aluno)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'})

# Define a rota para baixar os dados em formato CSV
@app.route('/download', methods=['GET'])
def download_csv():
    # Obtém os dados do Firestore
    alunos_ref = db.collection('alunos').get()
    alunos = [aluno.to_dict() for aluno in alunos_ref]
    # Converte os dados em um DataFrame do pandas
    df = pd.DataFrame(alunos)
    # Gera um arquivo CSV a partir do DataFrame
    csv = df.to_csv(index=False)
    # Cria uma resposta HTTP com o arquivo CSV
    response = make_response(csv)
    response.headers['Content-Disposition'] = 'attachment; filename=dados.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

# Define a rota para fazer o upload de dados a partir de um arquivo CSV
@app.route('/upload', methods=['POST'])
def upload_csv():
    # Obtém o arquivo CSV do corpo da requisição
    file = request.files['file']
    # Lê o arquivo CSV com o pandas
    df = pd.read_csv(file)
    # Itera sobre as linhas do DataFrame e adiciona cada linha ao Firestore
    for _, row in df.iterrows():
        db.collection('alunos').add(row.to_dict())
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Dados adicionados com sucesso!'})

# Define a rota para atualizar os dados de um aluno
@app.route('/alunos/<aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    # Obtém os novos dados do aluno a partir do corpo da requisição
    novos_dados = request.json
    # Atualiza os dados do aluno no Firestore
    db.collection('alunos').document(aluno_id).update(novos_dados)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Dados do aluno atualizados com sucesso!'})

# Define a rota para cadastrar um professor
@app.route('/professores', methods=['POST'])
def cadastrar_professor():
    # Obtém os dados do professor a partir do corpo da requisição
    professor = request.json
    # Adiciona o professor ao Firestore
    db.collection('professores').add(professor)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Professor cadastrado com sucesso!'})

# Define a rota para cadastrar uma disciplina
@app.route('/disciplinas', methods=['POST'])
def cadastrar_disciplina():
    # Obtém os dados da disciplina a partir do corpo da requisição
    disciplina = request.json
    # Adiciona a disciplina ao Firestore
    db.collection('disciplinas').add(disciplina)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Disciplina cadastrada com sucesso!'})

# Define a rota para cadastrar uma turma
@app.route('/turmas', methods=['POST'])
def cadastrar_turma():
    # Obtém os dados da turma a partir do corpo da requisição
    turma = request.json
    # Adiciona a turma ao Firestore
    db.collection('turmas').add(turma)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Turma cadastrada com sucesso!'})

# Define a rota para matricular um aluno em uma turma e disciplina
@app.route('/matriculas', methods=['POST'])
def matricular_aluno():
    # Obtém os dados da matrícula a partir do corpo da requisição
    matricula = request.json
    # Adiciona a matrícula ao Firestore
    db.collection('matriculas').add(matricula)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Aluno matriculado com sucesso!'})

# Define a rota para lançar notas e faltas de um aluno em uma turma e disciplina
@app.route('/notas-faltas', methods=['POST'])
def lancar_notas_faltas():
    # Obtém os dados das notas e faltas a partir do corpo da requisição
    notas_faltas = request.json
    # Atualiza as notas e faltas do aluno no Firestore
    db.collection('matulas').document(notas_faltas['matricula_id']).update(notas_faltas)
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'Notas e faltas lançadas com sucesso!'})

# Define a rota para gerar um boletim de desempenho de um aluno em uma turma e disciplina
@app.route('/boletim/<matricula_id>', methods=['GET'])
def gerar_boletim(matricula_id):
    # Obtém os dados da matrícula a partir do ID da matrícula fornecido na requisição
    matricula_ref = db.collection('matriculas').document(matricula_id).get()
    matricula = matricula_ref.to_dict()
    # Obtém os dados do aluno a partir ID do aluno na matrícula
    aluno_ref = db.collection('alunos').document(matricula['aluno_id']).get()
    aluno = aluno_ref.to_dict()
    # Obtém os dados da disciplina a partir do ID da disciplina na matrícula
    disciplina_ref = db.collection('disciplinas').document(matricula['disciplina_id']).get()
    disciplina = disciplina_ref.to_dict()
    # Obtém os dados da turma a partir do ID da turma na matrícula
    turma_ref = db.collection('turmas').document(matricula['turma_id']).get()
    turma = turma_ref.to_dict()
    # Calcula a média do aluno na disciplina
    media = sum(matricula['notas']) / len(matricula['notas'])
    # Cria um dicionário com os dados do boletim
    boletim = {
        'aluno': aluno,
        'disciplina': disciplina,
        'turma': turma,
        'notas': matricula['notas'],
        'faltas': matricula['faltas'],
        'media': media
    }
    # Retorna o boletim em formato JSON
    return jsonify(boletim)

# Define a rota para gerar um relatório de desempenho de todos os alunos em uma turma e disciplina
@app.route('/relatorio/<turma_id>/<disciplina_id>', methods=['GET'])
def gerar_relatorio(turma_id, disciplina_id):
    # Obtém as matrículas dos alunos na turma e disciplina especificadas
    matriculas_ref = db.collection('matriculas').where('turma_id', '==', turma_id).where('disciplina_id', '== disciplina_id).get()')
    matriculas = [matricula.to_dict() for matricula in matriculas_ref]
    # Obtém os dados da disciplina
    disciplina_ref = db.collection('disciplinas').document(disciplina_id).get()
    disciplina = disciplina_ref.to_dict()
    # Obtém os dados da turma
    turma_ref = db.collection('turmas').document(turma_id).get()
    turma = turma_ref.to_dict()
    # Cria uma lista com os dados de desempenho de cada aluno
    desempenho_alunos = []
    for matricula in matriculas:
        # Obtém os dados do aluno
        aluno_ref = db.collection('alunos').document(matricula['aluno_id']).get()
        aluno = aluno_ref.to_dict()
        # Calcula a média do aluno na disciplina
        media = sum(matricula['notas']) / len(matricula['notas'])
        # Adiciona os dados de desempenho do aluno à lista
        desempenho_aluno = {
            'aluno': aluno,
            'notas': matricula['notas'],
            'faltas': matricula['faltas'],
            'media': media
        }
        desempenho_alunos.append(desempenho_aluno)
    # Cria um dicionário com os dados do relatório
    relatorio = {
        'disciplina': disciplina,
        'turma': turma,
        'desempenho_alunos': desempenho_alunos
    }
    # Retorna o relatório em formato JSON
    return jsonify(relatorio)

# Define a rota para calcular o IMC de cada aluno
@app.route('/imc', methods=['GET'])
def calcular_imc():
    # Obtém os dados de todos os alunos do Firestore
    alunos_ref = db.collection('alunos').get()
    alunos = [aluno.to_dict() for aluno in alunos_ref]
    # Calcula o IMC de cada aluno
    for aluno in alunos:
        altura = aluno['altura']
        peso = aluno['peso']
        imc = peso / (altura ** 2)
        aluno['imc'] = imc
        # Atualiza os dados do aluno no Firestore
        db.collectionalunos.document(aluno['id']).update({'imc':imc})
    # Retorna uma mensagem de sucesso
    return jsonify({'mensagem': 'IMC calculado com sucesso!'})

if __name__ == '__main__':
    app.run()