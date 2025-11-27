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
from utils.utilitarios import evidencia, verificar_mudanca, capturar_estado, baixar_imagem_aleatoria

fake = fk()  # Instancia o Faker para gerar dados aleatórios


@when("enviar produtos")
def step_impl(context):
    """Abre o modal uma vez antes do loop e cadastra múltiplos produtos.
    A cada iteração, verifica se o modal está aberto. Se fechou, reabre.
    """
    
    # Abre o modal ANTES do loop
    botao = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/header/button')
    estado_antes = capturar_estado(context.driver)
    botao.click()
    
    # Aguarda o modal abrir pela primeira vez
    modal_aberto = verificar_mudanca(context.driver, estado_antes, timeout=5, verificar_url=False)
    
    if not modal_aberto:
        print("❌ ERRO: Modal não abriu na primeira tentativa")
        evidencia(context, 'Cadastro_massa_FALHA_modal_inicial')
        context.driver.quit()
        assert False, "Modal de cadastro não abriu"
    
    print("✅ Modal aberto - Iniciando cadastro em massa")
    time.sleep(1)
    
    qtd_produtos = 10

    prod = {
        'passou' : [],
        'falhou' : []
    }

    # Loop para cadastrar múltiplos produtos
    for i in range(qtd_produtos):
        print(f"\n{'─'*60}")
        print(f"📦 Produto {i+1}/{qtd_produtos}")
        print(f"{'─'*60}")
        
        # Verifica se o modal está aberto (pode ter fechado após envio anterior)
        modal_presente = context.driver.find_elements(By.XPATH, "//div[@role='dialog' and @data-state='open']")
        
        if not modal_presente:
            print(f"⚠️ Modal fechou após produto {i} - Reabrindo...")
            botao = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/header/button')
            botao.click()
            time.sleep(2)  # Aguarda modal reabrir
        else:
            print("✅ Modal já está aberto")

        """Preenche o formulário de cadastro de produto com dados aleatórios.
        Gera nome, descrição, categoria, preço e frete aleatórios usando Faker.
        Gera uma imagem JPEG de 0.5MB automaticamente usando a função gerar_imagem_com_tamanho().
        """
        # Gera um nome aleatório para o produto
        nome = fake.name()
        
        imagem = baixar_imagem_aleatoria()

        # Localiza todos os campos do formulário de cadastro de produto
        form = {
        'nome' : context.driver.find_element(By.NAME, 'name'),  # Campo nome do produto
        'description' : context.driver.find_element(By.NAME, 'description'),  # Campo descrição
        'categoria' : context.driver.find_elements(By.XPATH, "//div[contains(@class,'sc-dAbbOL')]//label"),  # Checkboxes de categoria
        'preco' : context.driver.find_element(By.NAME, 'price'),  # Campo preço
        'imagem' : context.driver.find_element(By.NAME, 'image'),  # Input file para upload
        'frete' : context.driver.find_element(By.NAME, 'shipment'),  # Campo frete
        }
        
        # Seleciona a categoria e captura o texto do span
        indice_categoria = i % 3
        categoria_label = form['categoria'][indice_categoria]
        
        # Extrai o texto da categoria do span antes de clicar
        categoria_texto = categoria_label.find_element(By.TAG_NAME, 'span').text
        
        # Preenche cada campo do formulário com dados aleatórios
        form['nome'].send_keys(nome)  # Nome aleatório gerado
        form['description'].send_keys(categoria_texto)  # Usa o texto da categoria como descrição
        categoria_label.click()  # Clica na categoria selecionada
        form['preco'].send_keys(fake.random_int(min=0))  # Preço aleatório >= 0
        form['imagem'].send_keys(imagem)  # Caminho absoluto da imagem gerada
        form['frete'].send_keys(fake.random_int(min=0))  # Frete aleatório >= 0

        time.sleep(2)  # Aguarda preenchimento dos campos

        """Localiza e clica no botão de 'Enviar' ou 'Salvar' para submeter
        o formulário de cadastro do produto. Não aguarda resposta aqui.
        """
        # Localiza o botão de enviar/submeter o formulário
        context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/div[1]/div/form/button').click()
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
        if "sucesso" in mensagem.lower():
            print(f"✅ Cadastrado: {nome}")
            prod['passou'].append(f'{nome} teste: {i+1}')
        elif "erro" in mensagem.lower():
            print(f"❌ Erro: {nome}")
            evidencia(context, 'Cadastro_produto_ERRO_ao_enviar')
            prod['falhou'].append(f'{nome} teste: {i+1}')
        else:
            print(f"⚠️  Mensagem inesperada: {mensagem}")
            evidencia(context, 'Cadastro_produto_AVISO_mensagem_inesperada')
            prod['falhou'].append(f'{nome} teste: {i+1}')
    
    context.produtos = prod




@then("deve ver os produtos cadastrados")
def erro(context):
    """Exibe resumo dos produtos cadastrados com sucesso e falhas."""
    passaram = context.produtos['passou']
    falharam = context.produtos['falhou']  # Corrigido: era 'falhou' no dicionário

    print("\n" + "="*60)
    print("📊 RESUMO DO CADASTRO EM MASSA")
    print("="*60)
    
    print(f"\n✅ Produtos cadastrados com SUCESSO: {len(passaram)}")
    if passaram:
        for produto in passaram:
            print(f"   • {produto}")
    
    print(f"\n❌ Produtos que FALHARAM: {len(falharam)}")
    if falharam:
        for produto in falharam:
            print(f"   • {produto}")
    
    print("="*60)
    
    # Captura evidência final
    evidencia(context, 'Cadastro_massa_FINAL')

    print("Requisito que inspirou este teste: RF0004\n")

    time.sleep(2)
    # Fecha o navegador
    context.driver.quit()