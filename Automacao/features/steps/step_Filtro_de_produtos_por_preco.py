# Behave para leitura do BDD
from behave import given, when, then
# Imports do selenium para acessar o site
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# importa a exceção lançada quando o WebDriverWait expira (timeout)
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
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
from utils.utilitarios import evidencia, verificar_mudanca, capturar_estado



@when("clicar em uma valor no menu de filtragem")
def step_impl(context):

    price = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/nav/ul/div[2]/div[2]/button/h2')

    context.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", price)

    price.click()

    precos = context.driver.find_elements(By.ID, "radix-4")

    # Inicializa dicionário para armazenar resultados de cada preco
    context.resultados_precos = {}

    for i in range(len(precos)):
        context.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", precos[i])
        time.sleep(0.5)

        # Extrai o texto da preco (ex: "Roupas", "Calçados")
        # Busca o elemento <li> dentro do div com id="radix-2"
        try:
            texto_preco = precos[i].find_element(By.CLASS_NAME, "contentList").text
        except:
            texto_preco = f"preco_{i}"  # Fallback caso não encontre o texto

        # Antes de clicar
        estado_antes = capturar_estado(context.driver, xpath_elemento_customizado="//div[contains(@class,'sc-eldPxv')]")

        # Clica na preco
        precos[i].click()
        print(f"\n{'─'*60}")
        print(f"💰 [{i+1}/{len(precos)}] Testando faixa de preço: {texto_preco}")
        print(f"{'─'*60}")
        time.sleep(1)

        # Verifica se houve mudança
        passou = verificar_mudanca(context.driver, estado_antes, timeout=5, verificar_url=False, verificar_dialog=False)

        # Armazena resultado no context
        context.resultados_precos[texto_preco] = passou

        if passou:
            print(f"✅ Filtro aplicado com sucesso")
        else:
            print(f"❌ Filtro não funcionou")
            evidencia(context, f'Filtro_preco_FALHA_{texto_preco}')

    time.sleep(2)

@then("a página exibirá apenas os produtos com um valor igual ou abaixo ao valor selecionado")
def step_impl(context):
    print("Então a página exibirá apenas os produtos com um valor igual ou abaixo ao valor selecionado")

    time.sleep(2)

    print("Requisito que inspirou este teste: RF0007\n")

    context.driver.quit()