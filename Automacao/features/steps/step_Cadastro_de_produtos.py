# ============================================================================
# ARQUIVO: step_Cadastro_de_produtos.py
# PROPÓSITO: Testar cadastro de novos produtos no sistema
# CENÁRIO: Administrador logado acessa formulário de produto, preenche dados
#          com informações aleatórias e imagem gerada, e submete o cadastro
# ============================================================================

# Behave para leitura do BDD
from behave import given, when, then
# Imports do selenium para acessar o site
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# importa time para fazer esperas relacionadas ao relógio do computador
import time
# importa faker para realizar cadastros com dados falsos
from faker import Faker as fk
# importa pandas para demonstar dados de forma organizada no terminal
import pandas as pd
# importa os para acessar a pasta de evidencias
import os
# iimporta o pillow para gerar uma imagem
from PIL import Image as img
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia, obter_usuario, gerar_imagem_com_tamanho

fake = fk()  # Instancia o Faker para gerar dados aleatórios


@when("clicar no botão adicionar")
def step_impl(context):
    """Localiza e clica no botão 'Adicionar' ou '+' que abre o modal/formulário
    para cadastrar um novo produto. Aguarda 2 segundos após o clique.
    """
    # Localiza o botão de adicionar produto pelo XPath
    botao = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/header/button')

    botao.click()  # Clica no botão
    time.sleep(2)  # Aguarda abertura do formulário


@when("preencher todos os dados obrigatórios")
def dados(context):
    """Preenche o formulário de cadastro de produto com dados aleatórios.
    Gera nome, descrição, categoria, preço e frete aleatórios usando Faker.
    Gera uma imagem JPEG de 0.5MB automaticamente usando a função gerar_imagem_com_tamanho().
    """
    # Gera um nome aleatório para o produto
    nome = fake.name()


    # ===== OPÇÃO ALTERNATIVA: Usar imagem existente (comentada) =====
    # Para usar uma imagem já existente na pasta imagem_produto/:
    """
    produto = 'produto.jpg'  # Nome do arquivo de imagem
    _, caminho_atual = obter_usuario()  # Obtém caminho da pasta utils

    img = os.path.abspath(caminho_atual, '..','..', 'imagem_produto', produto)
    """

    # ===== OPÇÃO ATIVA: Gerar imagem nova automaticamente =====
    print("\n📝 Preenchendo formulário...")
    print("🖼️  Gerando imagem do produto...")
    # Gera uma imagem JPEG de 0.5MB com nome aleatório
    # Parâmetros: (tamanho_em_mb, nome_arquivo_sem_extensão)
    imagem, tamanho_gerado = gerar_imagem_com_tamanho(0.9, nome)
    
    # Salva informações no context para usar depois
    context.produto_nome = nome
    context.produto_imagem = imagem
    context.produto_tamanho_mb = tamanho_gerado

    # Localiza todos os campos do formulário de cadastro de produto
    form = {
       'nome' : context.driver.find_element(By.NAME, 'name'),  # Campo nome do produto
       'description' : context.driver.find_element(By.NAME, 'description'),  # Campo descrição
       'categoria' : context.driver.find_elements(By.XPATH, "//div[contains(@class,'sc-dAbbOL')]//label"),  # Checkboxes de categoria
       'preco' : context.driver.find_element(By.NAME, 'price'),  # Campo preço
       'imagem' : context.driver.find_element(By.NAME, 'image'),  # Input file para upload
       'frete' : context.driver.find_element(By.NAME, 'shipment'),  # Campo frete
    }
    
    # Preenche cada campo do formulário com dados aleatórios
    form['nome'].send_keys(nome)  # Nome aleatório gerado
    form['description'].send_keys('teste')  # Descrição fixa
    form['categoria'][fake.random_int(0, 2)].click()  # Seleciona categoria aleatória (0, 1 ou 2)
    form['preco'].send_keys(fake.random_int(min=0))  # Preço aleatório >= 0
    form['imagem'].send_keys(imagem)  # Caminho absoluto da imagem gerada
    form['frete'].send_keys(fake.random_int(min=0))  # Frete aleatório >= 0

    time.sleep(2)  # Aguarda preenchimento dos campos

   
@when("clicar em enviar novo o produto")
def enviar(context):
    """Localiza e clica no botão de 'Enviar' ou 'Salvar' para submeter
    o formulário de cadastro do produto. Não aguarda resposta aqui.
    """
    # Localiza o botão de enviar/submeter o formulário
    context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/div[1]/div/form/button').click()



@then("deve receber a mensagem de novo produto criado com sucesso")
def erro(context):
    """Aguarda e valida a mensagem toast de sucesso ou erro após envio do produto.
    Usa WebDriverWait para aguardar até 10 segundos pelo aparecimento do toast.
    Verifica se a mensagem contém 'sucesso' ou 'erro' e exibe no console.
    Captura screenshot da tela como evidência.
    """
    # Configura espera explícita de até 10 segundos
    wait = WebDriverWait(context.driver, 10)

    # Aguarda até que o toast (mensagem de feedback) apareça na tela
    # O toast tem role='status' e deve conter 'sucesso' ou 'Erro' no texto
    toast = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[@role='status' and (contains(text(),'sucesso') or contains(text(),'Erro'))]"
        ))
    )

    # Extrai o texto da mensagem e remove espaços em branco
    mensagem = toast.text.strip()

    # Valida a mensagem e exibe feedback no console
    print("\n" + "─"*60)
    if "sucesso" in mensagem.lower():
        print("✅ Produto cadastrado com sucesso")
    elif "erro" in mensagem.lower():
        print("❌ Erro ao cadastrar produto")
        evidencia(context, 'Cadastro_produto_ERRO_ao_enviar')
    else:
        print(f"⚠️  Mensagem inesperada: {mensagem}")
        evidencia(context, 'Cadastro_produto_AVISO_mensagem_inesperada')
    print("─"*60)

    # Captura screenshot da tela com o toast visível
    nome = 'Cadastro_de_produtos'
    evidencia(context, nome)

    print("Requisito que inspirou este teste: RF0004\n")

    time.sleep(2)
    # Fecha o navegador
    context.driver.quit()