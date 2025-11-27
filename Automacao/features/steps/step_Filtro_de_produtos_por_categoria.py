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

@when("clicar em uma categoria no menu de filtragem")
def step_impl(context):

    categorias = context.driver.find_elements(By.ID, "radix-2")

    # Inicializa dicionário para armazenar resultados de cada categoria
    context.resultados_categorias = {}

    for i in range(len(categorias)):
        indice = (i+1)%len(categorias) # formula para começar no indice 1, ir até o último indice e depois usar o indice 0
        # fiz essa lógica pois o primeiro filtro que é todos já vem selecionado, logo ele deve ser o último da lista
        context.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", categorias[indice])
        time.sleep(0.5)

        # Extrai o texto da categoria (ex: "Roupas", "Calçados")
        # Busca o elemento <li> dentro do div com id="radix-2"
        try:
            texto_categoria = categorias[indice].find_element(By.CLASS_NAME, "contentList").text
        except:
            texto_categoria = f"Categoria_{indice}"  # Fallback caso não encontre o texto

        # Antes de clicar
        estado_antes = capturar_estado(context.driver, xpath_elemento_customizado="//div[contains(@class,'sc-eldPxv')]")

        # Clica na categoria
        categorias[indice].click()
        print(f"\n{'─'*60}")
        print(f"🔍 [{i+1}/{len(categorias)}] Testando categoria: {texto_categoria}")
        print(f"{'─'*60}")
        time.sleep(1)

        # Verifica se houve mudança
        passou = verificar_mudanca(context.driver, estado_antes, timeout=5, verificar_url=False, verificar_dialog=False)

        # Armazena resultado no context
        context.resultados_categorias[texto_categoria] = passou

        if passou:
            print(f"✅ Filtro aplicado com sucesso")
        else:
            print(f"❌ Filtro não funcionou")
            evidencia(context, f'Filtro_categoria_FALHA_{texto_categoria}')


    time.sleep(2)

@then("a página exibirá apenas os produtos dessa categoria")
def step_impl(context):
    """Valida os resultados de todas as categorias testadas.
    Se alguma categoria falhou, captura evidência e FAZ O TESTE FALHAR.
    """
    
    print("\n" + "="*60)
    print("RESUMO DOS TESTES DE FILTRAGEM POR CATEGORIA")
    print("="*60)
    
    # Lista para armazenar categorias que falharam
    categorias_falharam = []
    
    # Exibe resultados de cada categoria
    for categoria, passou in context.resultados_categorias.items():
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        print(f"{status} - {categoria}")
        
        if not passou:
            categorias_falharam.append(categoria)
    
    print("="*60)
    print(f"\nRequisito que inspirou este teste: RF0006\n")

    # Captura evidência
    nome_evidencia = 'Filtro_de_produtos_por_categoria'
    if categorias_falharam:
        nome_evidencia += '_FALHOU'
    evidencia(context, nome_evidencia)
    
    time.sleep(2)
    context.driver.quit()
    
    # Se alguma categoria falhou, FAZ O TESTE FALHAR
    if categorias_falharam:
        categorias_str = ', '.join(categorias_falharam)
        assert False, f"Filtragem falhou para as categorias: {categorias_str}"