# ============================================================================
# ARQUIVO: step_Cadastro_apenas_para_administrador.py
# PROPÓSITO: Validar fluxo completo - cadastro via API + login web de administrador
# CENÁRIO: Cadastra usuário via API REST, faz login para obter token, e depois
#          faz login na interface web para acessar área administrativa
# ============================================================================

# Behave para leitura do BDD
from behave import given, when, then
# importa time para fazer esperas relacionadas ao relógio do computador
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# importa faker para realizar cadastros com dados falsos
from faker import Faker as fk
# importa pandas para demonstar dados de forma organizada no terminal
import pandas as pd
# importa as funções da api
from utils.api_functions import register, login
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia
# importa json para salvar credenciais
import json
import os

fake = fk()  # Instancia o Faker
# Gera dados aleatórios para o cadastro (usados em todo o fluxo)
dados = {
    'email' : fake.email(),
    'password' : fake.password()
}

@given("que o usuário deseja realizar cadastro via api")
def step_impl(context):
    """Realiza cadastro de novo usuário através da API REST usando endpoint POST /register.
    Envia email e senha gerados aleatoriamente pelo Faker.
    Exibe a mensagem de resposta da API no console.
    Cria automaticamente o arquivo user.json com as credenciais geradas.
    """
    # Chama função register() que faz POST para endpoint de cadastro
    msg = register(dados)
    # Exibe mensagem de resposta da API (ex: "Usuário cadastrado com sucesso")
    print(f'✅{msg['msg']}')
    
    # Cria o arquivo user.json com as credenciais geradas
    user_json_path = os.path.join('utils', 'user.json')
    user_data = {
        'usuario': dados['email'],
        'senha': dados['password']
    }
    
    with open(user_json_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)
    
    print(f'📝 Arquivo user.json criado com sucesso em utils/')
    print(f'📧 Email: {dados["email"]}')
    print(f'🔑 Senha: {dados["password"]}\n')
    
    time.sleep(2)

@when("chamar o método post no endpoint /login e passando os parametros de email e senha")
def step_impl(context):
    """Faz login via API REST usando endpoint POST /login com as credenciais
    cadastradas no step anterior. Recebe token de autenticação e dados do usuário.
    Salva os dados no context para usar nos próximos steps.
    Exibe a resposta completa em formato de DataFrame para visualização organizada.
    """
    # Chama função login() que faz POST para endpoint de login
    entrar = login(dados)

    # Salva resposta no context para acessar em outros steps
    context.entrar = entrar

    # Exibe mensagem de resposta (ex: "Login realizado com sucesso")
    print(f'✅{entrar['msg']}')

    # Exibe todos os dados retornados em formato tabular usando Pandas
    print(pd.DataFrame(entrar))

    time.sleep(2)

@then("receberá um token para validar o cadastro do usuário")
def step_impl(context):
    """Extrai e exibe o token JWT recebido no login via API.
    O token é usado para autenticar requisições subsequentes à API.
    """
    # Recupera os dados salvos no context pelo step anterior
    dados = context.entrar

    # Extrai o token da resposta
    token = dados['token']

    # Exibe o token no console
    print(f'O token é: {token}')

    time.sleep(2)
    pass

@when('o usuario preencher com os dados falsos')
def logar(context):
    """Realiza login na interface web usando as mesmas credenciais geradas
    anteriormente (dados aleatórios do Faker). Localiza os campos do formulário,
    preenche email e senha, e clica no botão de login.
    """
    # Usa os mesmos dados gerados no início do teste
    user = dados

    # Localiza os elementos do formulário de login na página web
    login = {
        'email' : context.driver.find_element(By.NAME, 'email'),
        'senha' : context.driver.find_element(By.NAME, 'password'),
        'entrar' : context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/button')
    }

    # Preenche os campos com as credenciais geradas
    login['email'].send_keys(user['email'])
    login['senha'].send_keys(user['password'])

    # Clica no botão de login
    login['entrar'].click()

    time.sleep(2)

@then('receberá a mensagem de login com sucesso')
def capturar_login(context):
    """Captura screenshot da tela após login bem-sucedido como evidência.
    A screenshot comprova que o usuário cadastrado via API conseguiu
    fazer login na interface web e acessar a área administrativa.
    """
    nome = 'Cadastro_apenas_para_administrador'
    # Salva screenshot na pasta evidencia/
    evidencia(context, nome)

    print("Requisito que inspirou este teste 'RF0003'\n")

    time.sleep(2)
    # Fecha o navegador
    context.driver.quit()    