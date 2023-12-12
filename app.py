from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

class Veiculo:
    def __init__(self, modelo, ano_fabricacao, qtd_portas, marca):
        self.modelo = modelo
        self.ano_fabricacao = ano_fabricacao
        self.qtd_portas = qtd_portas
        self.marca = marca

    def to_dict(self):
        return {
            'modelo': self.modelo,
            'ano_fabricacao': self.ano_fabricacao,
            'qtd_portas': self.qtd_portas,
            'marca': self.marca
        }

class Carro(Veiculo):
    def __init__(self, modelo, ano_fabricacao, qtd_portas, marca):
        if not (2 <= qtd_portas <= 4):
            raise ValueError("A quantidade de portas para um carro deve ser entre 2 e 4.")
        super().__init__(modelo, ano_fabricacao, qtd_portas, marca)

class Moto(Veiculo):
    def __init__(self, modelo, ano_fabricacao, marca):
        super().__init__(modelo, ano_fabricacao, 0, marca)
        self.rodas = 2
        self.passageiros = 0

    def set_passageiros(self, quantidade):
        if not (1 <= quantidade <= 2):
            raise ValueError("A quantidade de passageiros para uma moto deve ser entre 1 e 2.")
        self.passageiros = quantidade

    def to_dict(self):
        data = super().to_dict()
        data.update({'rodas': self.rodas, 'passageiros': self.passageiros})
        return data

def salvar_dados_em_arquivo(nome_arquivo, novo_dado):
    dados = []

    # Se o arquivo já existe, leia os dados existentes
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo_existente:
            dados = json.load(arquivo_existente)

    # Adicione o novo dado à lista
    dados.append(novo_dado)

    # Salve a lista completa no arquivo
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_carro', methods=['POST'])
def cadastrar_carro():
    try:
        modelo = request.form['modeloCarro']
        ano_fabricacao = request.form['anoCarro']
        marca = request.form['marcaCarro']
        qtd_portas = int(request.form['qtdPortasCarro'])
        carro = Carro(modelo, ano_fabricacao, qtd_portas, marca)

        # Salvar dados em um arquivo JSON sem substituir os existentes
        salvar_dados_em_arquivo('carro.json', carro.to_dict())

        return jsonify({'success': True, 'message': 'Carro cadastrado com sucesso!'})
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)})

@app.route('/cadastrar_moto', methods=['POST'])
def cadastrar_moto():
    try:
        modelo = request.form['modeloMoto']
        ano_fabricacao = request.form['anoMoto']
        marca = request.form['marcaMoto']
        moto = Moto(modelo, ano_fabricacao, marca)
        qtd_passageiros = int(request.form['qtdPassageirosMoto'])
        moto.set_passageiros(qtd_passageiros)

        # Salvar dados em um arquivo JSON sem substituir os existentes
        salvar_dados_em_arquivo('moto.json', moto.to_dict())

        return jsonify({'success': True, 'message': 'Moto cadastrada com sucesso!'})
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)})

if __name__ == '__main__':
    app.run(debug=True)
