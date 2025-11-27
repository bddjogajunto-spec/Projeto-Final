# ============================================================================
# ARQUIVO: step_Erro_de_login_social.py
# PROPÓSITO: Testar erro ao tentar login com Google/GitHub sem preencher email
# CENÁRIO: Usuário clica em "Entrar com Google" ou "Entrar com GitHub" e 
#          recebe mensagem de erro por não ter digitado email
# ============================================================================

# Behave para leitura do BDD
from behave import given, when, then
# Imports do selenium para acessar o site
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
# importa time para fazer esperas relacionadas ao relógio do computador
import time
# acessa a pasta de funções comuns para importar a evidencia
from utils.utilitarios import evidencia


@when('clica no Entrar com "{rede_social}"')
def login_social(context, rede_social):
    """Clica no botão de login social (Google ou GitHub) na página de login.
    O parâmetro {rede_social} vem do .feature file e determina qual botão clicar.
    Salva a rede social no context para usar no próximo step.
    """
    context.rede_social = rede_social  # Salva no context para usar na evidência depois
    
    # Seleciona o XPath correto baseado na rede social
    if rede_social == "Google":
        # XPath do botão "Entrar com Google"
        seletor = context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[5]/div/button[1]')
    else:  # GitHub
        # XPath do botão "Entrar com GitHub"
        seletor = context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[5]/div/button[2]')
    
    seletor.click()  # Clica no botão selecionado
    time.sleep(2)  # Aguarda processamento do clique

@then("recebe erro de email não digitado para login")
def captura_evidencia(context):
    """Captura screenshot da mensagem de erro exibida quando o usuário tenta
    login social sem ter digitado o email. O nome da evidência inclui a rede social
    que foi usada (Google ou GitHub).
    """
    # Recupera a rede social que foi salva no step anterior
    rede_social = context.rede_social
    # Cria nome descritivo para o arquivo de evidência
    nome = f"erro_login_{rede_social}"
    # Tira screenshot e salva na pasta evidencia/
    evidencia(context, nome)

    print("Requisito que inspirou este teste: NF0004\n")

    time.sleep(2)
    # Fecha o navegador ao finalizar o teste
    context.driver.quit()