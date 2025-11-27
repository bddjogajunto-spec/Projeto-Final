# ============================================================================
# ARQUIVO: step_comum.py
# PROPÓSITO: Centralizar steps COMPARTILHADOS entre múltiplos arquivos .feature
# IMPORTANTE: Evita erro AmbiguousStep quando o mesmo step aparece em vários testes
# ============================================================================

# Behave para leitura do BDD
from behave import given
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
# importa time para fazer esperas relacionadas ao relógio do computador
import time

from utils.utilitarios import obter_usuario, verificar_mudanca, capturar_estado, evidencia


@given("que o usuário está na página de login")
def step_impl(context):
    """Abre o navegador Edge e acessa a página de login do sistema.
    Configurações do Edge:
    - Maximiza a janela
    - Desabilita detecção de automação
    - Remove logs de console do WebDriver
    """
    print("\n" + "─"*60)
    print("🌐 Iniciando navegador...")
    # Configurações do navegador Edge
    options=Options()
    options.add_argument("--Start-maximized")  # Abre em tela cheia
    options.add_argument("--disable-blink-features=AutomationControlled")  # Esconde que é automação
    options.add_experimental_option("excludeSwitches",["enable-logging"])  # Remove logs do console

    # Inicializa o driver e salva no context para usar em outros steps
    context.driver = Edge(options=options)
    # Navega para a URL do sistema
    context.driver.get("https://projetofinal.jogajuntoinstituto.org/")
    print("✅ Página de login carregada")
    print("─"*60)
    time.sleep(3)  # Aguarda carregamento completo

@given("que o usuário está na página de /products")
def step_impl(context):
    """Abre o navegador, acessa a página de login e já faz o login automático
    para chegar na página de produtos (/products).
    Usa credenciais do arquivo user.json através da função obter_usuario().
    """
    print("\n" + "─"*60)
    print("🌐 Iniciando navegador...")
    # Configurações do navegador Edge
    options=Options()
    options.add_argument("--Start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches",["enable-logging"])

    # Inicializa driver e acessa página inicial
    context.driver = Edge(options=options)
    context.driver.get("https://projetofinal.jogajuntoinstituto.org/")

    time.sleep(2)

    print("✅ Página de login carregada")
    print("🔐 Realizando login automático...")

    # Obtém credenciais do arquivo user.json
    dados, _ = obter_usuario()

    # Localiza os elementos do formulário de login
    login = {
        'email' : context.driver.find_element(By.NAME, 'email'),
        'senha' : context.driver.find_element(By.NAME, 'password'),
        'entrar' : context.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/button')
    }

    # Preenche os campos com as credenciais
    login['email'].send_keys(dados['usuario'])
    login['senha'].send_keys(dados['senha'])

    # Captura estado ANTES do clique no botão de login
    estado_antes = capturar_estado(context.driver)

    # Clica no botão de login
    login['entrar'].click()

    # Verifica se houve mudança após o login (navegação ou modal)
    login_sucesso = verificar_mudanca(context.driver, estado_antes, timeout=5)

    if login_sucesso:
        print("✅ Login realizado com sucesso")
        print("✅ Página de produtos carregada")
        print("─"*60)
    else:
        print("❌ ERRO: Login falhou - nenhuma mudança detectada")
        evidencia(context, 'Login_FALHA_sem_mudanca')
        context.driver.quit()
        assert False, "Login falhou - nenhuma navegação ou mudança foi detectada após clicar em entrar"

    time.sleep(2)