# ============================================================================
# ARQUIVO: step_Impedir_cadastro_de_usuario_externo.py
# PROPÓSITO: Validar que usuários externos NÃO conseguem criar conta no sistema
# CENÁRIO: Usuário tenta criar conta na página de cadastro e verifica se 
#          recebe mensagem de "cadastrado com sucesso" (esperado: NÃO deve permitir)
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
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia, capturar_estado, verificar_mudanca
fake = fk()  # Instancia o Faker para gerar dados aleatórios

@when("ele acessar a página de cadastro")
def acessar_register(context):
    """Navega da página de login para a página de cadastro clicando no link
    'Criar conta' ou equivalente. Aguarda carregamento da nova página.
    """
    print("\n" + "─"*60)
    print('🌐 Acessando página de cadastro...')
    # Localiza e clica no link que leva à página de cadastro
    context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[6]/span[2]/a').click()
    time.sleep(2)
    print('✅ Página de cadastro carregada')
    print("─"*60)
    time.sleep(2)



@when("tentar criar conta")
def step_impl(context):
    """Preenche o formulário de cadastro com dados aleatórios gerados pelo Faker
    e tenta submeter o cadastro. Gera email, senha e confirmação de senha automáticos.
    """
    # Localiza todos os campos do formulário de cadastro
    form = {
        'email' : context.driver.find_element(By.NAME, 'email'),
        'senha' : context.driver.find_element(By.NAME, 'password'),
        'confirma' : context.driver.find_element(By.NAME, 'confirmPassword'),
        'botao' : context.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/button')
    }

    # Gera uma senha aleatória
    senha = fake.password()

    # Preenche os campos do formulário
    form['email'].send_keys(fake.email())  # Email aleatório
    form['senha'].send_keys(senha)  # Senha gerada
    form['confirma'].send_keys(senha)  # Confirmação da mesma senha
    
    form['botao'].click()  # Clica no botão de cadastrar
    time.sleep(2)  # Aguarda resposta do servidor

@then("receberá a mensagem de cadastrado com sucesso")
def step_impl(context):
    """Valida que o sistema NÃO deve permitir cadastro de usuário externo.
    Se detectar a mensagem de sucesso, o teste FALHA.
    """
    
    print("\n" + "="*60)
    
    # Busca pela mensagem de sucesso específica
    mensagem_sucesso = context.driver.find_elements(By.XPATH, "//span[@class='sucess' and contains(text(), 'Usuário cadastrado com sucesso')]")
    
    if len(mensagem_sucesso) > 0:
        print("❌ ERRO: Sistema permitiu cadastro de usuário externo")
        print("   Esperado: Bloqueio de cadastro")
        print("   Obtido: 'Usuário cadastrado com sucesso'")
        evidencia(context, 'Impedir_cadastro_externo_ERRO_permitiu_cadastro')
        print("="*60)
        
        nome = 'Impedir_cadastro_de_usuario_externo_FALHOU'
        evidencia(context, nome)
        
        print("Requisito que inspirou este teste: RF0001\n")
        
        time.sleep(2)
        context.driver.quit()
        
        assert False, "Sistema permitiu cadastro de usuário externo quando deveria bloquear"
    else:
        print("✅ Cadastro bloqueado corretamente - usuário externo não pôde criar conta")
        print("="*60)
        
        nome = 'Impedir_cadastro_de_usuario_externo_PASSOU'
        evidencia(context, nome)
        
        print("Requisito que inspirou este teste: RF0001\n")
        
        time.sleep(2)
        context.driver.quit()

