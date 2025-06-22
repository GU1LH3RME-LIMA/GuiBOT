import requests
from flask import Flask, request, render_template,jsonify
import os
from iagen import enviar_pergunta

app= Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
arquivo =None

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/anexar",methods=["POST"])

def anexar():
    global arquivo  # avisando que vamos usar/modificar a variável global
    file = request.files.get('arquivo')

    if file:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(caminho)
        arquivo = caminho  # atualiza a variável global com o caminho correto
        return jsonify({"success": True, "arquivo": f'Arquivo {file.filename} anexado com sucesso!'})
    
    return jsonify({"success": False, "arquivo": f'Erro ao anexar aquivo!'})


@app.route("/enviar", methods=["POST"])
def enviarPergunta():
    global arquivo  # necessário para acessar a variável global corretamente
    pergunta = request.form.get("pergunta") 
    resposta = enviar_pergunta(pergunta, arquivo)

    return jsonify({"success": True, "resposta": resposta})
