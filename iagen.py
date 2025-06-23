import os
import time
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

# Configuração da API
api_key = 'Coloque a API aqui'
os.environ["GROQ_API_KEY"] = api_key
chat = ChatGroq(model='llama-3.3-70b-versatile')

def processar_em_streaming(documento):
    for pagina in documento:
        yield pagina  # Envia uma página por vez

template = ChatPromptTemplate.from_messages([
    ('system', 'Você é uma assistente virtual chamada GuiBOT que fornece informações de forma resumida e tem acesso às seguintes informações: {documento_atual} e {respostas_anteriores} '),
    ('user', '{input}')
])

chain = template | chat
cache = {}
respostas = ""

def enviar_pergunta(pergunta,arquivo):  
    global cache
    global respostas
    if pergunta in cache:
        return cache[pergunta]
    try:
        for documento_atual in processar_em_streaming(arquivo):
            resposta = chain.invoke({'documento_atual': documento_atual,'respostas_anteriores':respostas, 'input': pergunta})
            if (resposta.content is not None):
                break
            time.sleep(1.5)  # Pequeno atraso para evitar sobrecarga na API
        respostas+=resposta.content

    # Filtragem de respostas repetidas e combinação final
        resposta_final =resposta.content
        cache[pergunta] = resposta.content
        return resposta_final
    except Exception as e:
        return "Erro ao processar arquivo"
