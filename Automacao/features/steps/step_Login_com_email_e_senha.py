# ============================================================================
# ARQUIVO: step_Login_com_email_e_senha.py
# PROPÓSITO: Testar login de administrador com email e senha
# CENÁRIO: Administrador faz login com credenciais válidas e é redirecionado
#          para a página de produtos (/products)
# ============================================================================

# Behave para leitura do BDD
from behave import given, when, then
# Imports do selenium para acessar o site
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# importa time para fazer esperas relacionadas ao relógio do computador
import time
# importa faker para realizar cadastros com dados falsos
from faker import Faker as fk
# importa pandas para demonstar dados de forma organizada no terminal
import pandas as pd
# importa os para acessar a pasta de evidencias
import os
# importa json para abrir arquivos de utilidade
import json
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia, obter_usuario


@given("que o Usuário possui conta de administrador cadastrada")
def step_impl(context):
    """Abre o navegador Edge e acessa a página de login do sistema.
    Este step prepara o ambiente para o teste de login de administrador.
    Configura o Edge para maximizar tela e desabilitar detecção de automação.
    """
    print("\n" + "─"*60)
    print("🌐 Iniciando navegador...")
    # Configurações do navegador Edge
    options=Options()
    options.add_argument("--Start-maximized")  # Abre em tela cheia
    options.add_argument("--disable-blink-features=AutomationControlled")  # Esconde automação
    options.add_experimental_option("excludeSwitches",["enable-logging"])  # Remove logs

    # Inicializa o driver Edge
    context.driver = Edge(options=options)
    # Navega para a página de login
    context.driver.get("https://projetofinal.jogajuntoinstituto.org/")
    print("✅ Página de login carregada")
    print("─"*60)
    time.sleep(3)


@when("tentar logar com seu email e senha")
def step_impl(context):
    """Preenche o formulário de login com as credenciais de administrador
    obtidas do arquivo user.json e submete o login.
    Usa a função obter_usuario() para ler as credenciais do arquivo.
    """
    # Obtém as credenciais do arquivo user.json (retorna tupla, pega só o primeiro elemento)
    user, _ = obter_usuario()
    
    # Localiza os elementos do formulário de login
    login = {
        'email' : context.driver.find_element(By.NAME, 'email'),
        'senha' : context.driver.find_element(By.NAME, 'password'),
        'entrar' : context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/button')
    }

    # Preenche os campos com as credenciais do administrador
    login['email'].send_keys(user['usuario'])
    login['senha'].send_keys(user['senha'])

    # Clica no botão de login
    login['entrar'].click()

    time.sleep(2)

@then("deverá ser redirecionado para a página de cadastro de produtos")
def step_impl(context):
    """Verifica se o login foi bem-sucedido capturando screenshot da página
    de produtos (/products). A evidência comprova que o administrador
    conseguiu acessar a área restrita do sistema.
    """
    nome = 'Login_com_email_e_senha'
    # Captura screenshot da página de produtos
    evidencia(context, nome)

    print("Requisito que inspirou este teste: RF0002\n")

    time.sleep(2)
    # Fecha o navegador
    context.driver.quit()