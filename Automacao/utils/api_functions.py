'''
Swagger
{
    site : https://apipf.jogajuntoinstituto.org
    get : "/swagger"
    get : "/api"
    post : "/login"
    post : "/register"
    get :"/"
    post :"/"
    delete :"/{productId}"
}
'''

import requests
import pandas as pd

# Configurações do pandas para exibir todas as colunas e linhas
pd.set_option('display.max_columns', None)  # Mostra todas as colunas
pd.set_option('display.max_rows', None)     # Mostra todas as linhas
pd.set_option('display.width', None)        # Largura automática
pd.set_option('display.max_colwidth', None) # Mostra conteúdo completo das células



def get_request(endpoint):
    get = requests.get(endpoint)
    #get.raise_for_status()
    return get

""" def post_request(endpoint, dict):
    post = requests.post(endpoint, json=dict)
    return post.json() """


def login(dados):
    endpoint = 'https://apipf.jogajuntoinstituto.org/login'
    post = requests.post(endpoint, json=dados )
    return post.json()

def register(dados):
    endpoint = 'https://apipf.jogajuntoinstituto.org/register'
    post = requests.post(endpoint, json=dados)
    return post.json()


def cadastro(dados, autentica, imagem):
    endpoint = 'https://apipf.jogajuntoinstituto.org/'
    with open(imagem, "rb") as img:
        files = {
            'image' : img
        }
        post = requests.post(endpoint, headers=autentica, data=dados, files=files)

    return post.json()

def listar_produtos(autentica):
    endpoint = 'https://apipf.jogajuntoinstituto.org/'
    get = requests.get(endpoint, headers=autentica)
    return get.json()

def deletar_produto(autentica, id):
    endpoint = 'https://apipf.jogajuntoinstituto.org/'+str(id)
    get = requests.delete(endpoint, headers=autentica)

def main():
    api = get_request("https://apipf.jogajuntoinstituto.org/api")
    print(f"api status = {api}")

    dados_login = {
        'email' : "bdd@admin.com",
        'password' : "admin123"
    }

    resposta_login = login(dados_login)
    print(resposta_login['msg'])

    token = resposta_login['token']
    #print(f'O token é {token}')
    autentica = {
        "Authorization" : f'Bearer {token}'
    }

    dados_produto = {
        "name": "TENIS",
        "description": "Tenis Adidas Vecty",
        "price": "20.00",
        "category": "Acessórios",
        "shipment": "50.00"
    }

    caminho = "C:/Users/LeoPardo/Downloads/a_gere_uma_imagem_para.png"

    resposta_cadastro = cadastro(dados_produto, autentica, caminho)

    print(resposta_cadastro)

    lista = listar_produtos(autentica)

    print(pd.DataFrame(lista))
    for id in lista:
        deletar_produto(autentica, id['idprodutos'])

    lista = listar_produtos(autentica)
    print(pd.DataFrame(lista))

    resposta_cadastro = cadastro(dados_produto, autentica, caminho)


if __name__ == '__main__':
    main()
