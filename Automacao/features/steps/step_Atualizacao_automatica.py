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
from utils.utilitarios import evidencia, capturar_estado, verificar_mudanca



@when("o estoque mudar")
def step_impl(context):
    """Localiza todos os produtos na grid da página e clica no primeiro produto.
    Após o clique, usa capturar_estado() + verificar_mudanca() para detectar se houve navegação
    ou abertura de modal. Salva o resultado em context.passou para controlar
    a execução dos próximos steps.
    
    Se nenhum produto for encontrado, marca context.passou = False.
    Se o clique não gerar nenhuma ação, também marca False e os próximos steps são pulados.
    """
    # Localiza todos os produtos na grid usando XPath (busca por classe parcial)
    produtos = context.driver.find_elements(By.XPATH, "//div[contains(@class,'sc-eldPxv')]")

    if produtos:
        # Se encontrou produtos, pega o primeiro da lista
        primeiro_produto = produtos[0]
        
        # Captura estado ANTES do clique
        estado_antes = capturar_estado(context.driver)
        
        # Clica no primeiro produto
        primeiro_produto.click()
        
        # Verifica se alguma ação foi disparada após o clique
        context.passou = verificar_mudanca(context.driver, estado_antes, timeout=5)
    else:
        # Caso não encontre nenhum produto na página
        print("Nenhum produto encontrado.")
        context.passou = False  # Marca como falha


    time.sleep(2)

@then("o site deve atualizar a informação automaticamente")
def step_impl(context):
    """Valida se recebeu mensagem de sucesso após salvar as alterações.
    Se context.passou == False, captura evidência e FAZ O TESTE FALHAR.
    Se passou == True, valida a mensagem de sucesso e captura evidência.
    """
    if context.passou == False:
        # Se o teste falhou antes, captura evidência e FALHA o teste
        print(f"\n❌ FALHA: Não foi possível abrir as informações do produto")
        evidencia(context=context, nome='Edicao_produto_FALHA_nao_abriu_informacoes')
        print(f"\n❌ FALHA: Não foi possível abrir as informações do produto")
        print(f"Requisito que inspirou este teste 'RF0010'\n")
        
        # Fecha o navegador
        context.driver.quit()
        
        # FAZ O TESTE FALHAR no relatório do Behave
        assert False, "Não foi possível abrir a página de informações do produto - botão/modal não encontrado"
    

    context.driver.quit()