import os
import time
import json
from PIL import Image # gera imagem jpg
import numpy as np # gera ruido
import io # mede o tamanho da imagem sem gerar arquivo
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests

def evidencia(context, nome):
    # Obtém o diretório do arquivo atual e navega até a pasta evidencia
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio_atual, '..', 'evidencia')
    caminho = os.path.abspath(caminho)  # Normaliza o caminho
    
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    
    
    nome_arquivo = f'{nome}_{time.strftime('%Y%m%d_%H%M%S')}.png'
    caminho_completo = os.path.join(caminho, nome_arquivo)
    
    print(f"Tentando salvar em: {caminho_completo}")
    context.driver.save_screenshot(caminho_completo)
    print(f"Evidência salva em: {caminho_completo}")

def obter_usuario():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    user = os.path.join(diretorio_atual, 'user.json')
    with open(user, 'r', encoding='utf-8') as arquivo:
        usuario = json.load(arquivo)
    
    return usuario, diretorio_atual

def gerar_imagem_com_tamanho(tamanho_mb, nome, tolerancia_kb=50):
    """Gera uma imagem JPEG com tamanho específico em MB.
    
    Args:
        tamanho_mb: Tamanho alvo em megabytes
        nome: Nome base do arquivo (sem extensão)
        tolerancia_kb: Tolerância em kilobytes (padrão: 50KB)
    
    Returns:
        tuple: (caminho_absoluto, tamanho_final_mb)
    
    IMPORTANTE: A imagem gerada terá tamanho MAIOR OU IGUAL ao solicitado,
    nunca menor. Tolerância máxima: tamanho_alvo + 0.05MB
    """
    alvo_bytes = tamanho_mb * 1024 * 1024
    tolerancia = tolerancia_kb * 1024
    limite_inferior = alvo_bytes  # Não aceita menor que o pedido
    limite_superior = alvo_bytes + tolerancia  # Aceita até +50KB

    # Define o caminho: volta uma pasta e cria/usa pasta imagem_produto
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_destino = os.path.join(diretorio_atual, '..', 'imagem_produto')
    caminho_destino = os.path.abspath(caminho_destino)
    
    # Verifica se a pasta existe, se não, cria
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)

    # Estimativa inicial de dimensões baseada no tamanho desejado
    # JPEG com ruído comprime aproximadamente 1:2 a 1:4
    pixels_necessarios = int((tamanho_mb * 1024 * 1024 * 3) ** 0.5)
    largura = altura = max(500, min(pixels_necessarios, 20000))
    
    qualidade = 85
    max_tentativas = 30
    melhor_imagem = None
    melhor_tamanho = 0
    melhor_qualidade = 85
    melhor_dimensao = largura
    
    print(f"🎯 Alvo: {tamanho_mb:.2f} MB (aceita: {tamanho_mb:.2f} - {(tamanho_mb + tolerancia_kb/1024):.2f} MB)")

    # Loop principal: ajusta dimensões E qualidade
    for tentativa in range(max_tentativas):
        # Gera nova imagem com as dimensões atuais
        array = np.random.randint(0, 255, (altura, largura, 3), dtype=np.uint8)
        img = Image.fromarray(array)
        
        # Testa com qualidade atual
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=qualidade)
        tamanho_atual = buffer.tell()
        
        # print(f"Tentativa {tentativa + 1}: {largura}x{altura}, Q={qualidade} -> {tamanho_atual / (1024*1024):.3f} MB")
        
        # Verifica se está no range aceitável (>= alvo e <= alvo + tolerância)
        if limite_inferior <= tamanho_atual <= limite_superior:
            print(f"✅ Imagem gerada: {tamanho_atual / (1024*1024):.3f} MB (tentativa {tentativa + 1})")
            melhor_imagem = img
            melhor_tamanho = tamanho_atual
            melhor_qualidade = qualidade
            break
        
        # Guarda a melhor tentativa que seja >= alvo (mesmo que exceda tolerância)
        if tamanho_atual >= limite_inferior:
            if melhor_tamanho == 0 or tamanho_atual < melhor_tamanho:
                melhor_imagem = img
                melhor_tamanho = tamanho_atual
                melhor_qualidade = qualidade
                melhor_dimensao = largura
        
        # Ajusta dimensões E qualidade baseado no erro
        diferenca = tamanho_atual - alvo_bytes
        erro_percentual = abs(diferenca) / alvo_bytes
        
        if tamanho_atual < limite_inferior:
            # Muito pequeno: AUMENTA dimensões OU DIMINUI qualidade
            if erro_percentual > 0.3:  # Erro > 30%
                # Aumenta dimensões significativamente
                fator = 1.2
                largura = int(largura * fator)
                altura = int(altura * fator)
                largura = min(largura, 20000)
                altura = min(altura, 20000)
            else:
                # Erro pequeno: apenas diminui qualidade (aumenta tamanho)
                qualidade = max(1, qualidade - 5)
        
        elif tamanho_atual > limite_superior:
            # Muito grande: DIMINUI dimensões OU AUMENTA qualidade
            if erro_percentual > 0.3:  # Erro > 30%
                # Diminui dimensões significativamente
                fator = 0.85
                largura = int(largura * fator)
                altura = int(altura * fator)
                largura = max(500, largura)
                altura = max(500, altura)
            else:
                # Erro pequeno: apenas aumenta qualidade (diminui tamanho)
                qualidade = min(100, qualidade + 5)
    
    # Se não convergiu perfeitamente, usa a melhor tentativa >= alvo
    if melhor_imagem is None or melhor_tamanho == 0:
        print(f"⚠️ Não conseguiu convergir, gerando com dimensões mínimas...")
        array = np.random.randint(0, 255, (500, 500, 3), dtype=np.uint8)
        melhor_imagem = Image.fromarray(array)
        melhor_qualidade = 1
        buffer = io.BytesIO()
        melhor_imagem.save(buffer, format="JPEG", quality=melhor_qualidade)
        melhor_tamanho = buffer.tell()

    # Salva o arquivo com a melhor configuração encontrada
    caminho_imagem = os.path.join(caminho_destino, f'{nome}_{time.strftime("%Y%m%d_%H%M%S")}.jpg')
    melhor_imagem.save(caminho_imagem, format="JPEG", quality=melhor_qualidade)
    
    imagem_absoluta = os.path.abspath(caminho_imagem)
    tamanho_final_mb = melhor_tamanho / (1024 * 1024)
    
    # Validação final
    if melhor_tamanho < limite_inferior:
        print(f"⚠️ AVISO: Imagem menor que solicitado: {tamanho_final_mb:.3f} MB < {tamanho_mb} MB")
    elif melhor_tamanho > limite_superior:
        print(f"⚠️ AVISO: Imagem maior que tolerância: {tamanho_final_mb:.3f} MB > {(tamanho_mb + tolerancia_kb/1024):.2f} MB")
    
    return imagem_absoluta, tamanho_final_mb

def capturar_estado(driver, xpath_dialog="//div[@role='dialog']", xpath_elemento_customizado=None):
    """
    Captura o estado atual da página para comparação posterior.
    
    Args:
        driver: WebDriver do Selenium
        xpath_dialog: XPath customizado para verificar dialogs/modals
        xpath_elemento_customizado: XPath de elemento específico para monitorar (ex: grid de produtos)
    
    Returns:
        dict: Dicionário com url, quantidade de dialogs, HTML da página e elemento customizado
    """
    estado = {
        'url': driver.current_url,
        'dialogs': len(driver.find_elements(By.XPATH, xpath_dialog)),
        'html': driver.page_source  # Captura HTML completo da página
    }
    
    # Se foi passado um XPath customizado, captura o HTML desse elemento específico
    if xpath_elemento_customizado:
        elementos = driver.find_elements(By.XPATH, xpath_elemento_customizado)
        estado['elemento_customizado'] = ''.join([el.get_attribute('outerHTML') for el in elementos])
        estado['quantidade_elementos'] = len(elementos)
    
    return estado

def verificar_mudanca(driver, estado_anterior, timeout=5, verificar_url=True, verificar_dialog=True, verificar_html=False, verificar_elemento_customizado=True, xpath_dialog="//div[@role='dialog']"):
    """
    Verifica se houve mudanças na página comparando com estado anterior.
    Use capturar_estado() ANTES da ação, execute a ação, depois chame esta função.
    
    Args:
        driver: WebDriver do Selenium
        estado_anterior: Dict retornado por capturar_estado()
        timeout: Tempo máximo de espera em segundos (padrão: 5)
        verificar_url: Se True, verifica mudança de URL (padrão: True)
        verificar_dialog: Se True, verifica aparecimento de dialog/modal (padrão: True)
        verificar_html: Se True, verifica mudança no HTML da página (padrão: False - pode ser lento)
        verificar_elemento_customizado: Se True e elemento foi capturado, verifica mudança nele (padrão: True)
        xpath_dialog: XPath customizado para o dialog
    
    Returns:
        bool: True se alguma mudança foi detectada, False caso contrário
    """
    try:
        def verificar_condicoes(d):
            # Verifica URL
            if verificar_url and d.current_url != estado_anterior['url']:
                return True
            
            # Verifica dialogs
            if verificar_dialog and len(d.find_elements(By.XPATH, xpath_dialog)) != estado_anterior['dialogs']:
                return True
            
            # Verifica HTML completo
            if verificar_html and d.page_source != estado_anterior['html']:
                return True
            
            # Verifica elemento customizado (ex: grid de produtos)
            if verificar_elemento_customizado and 'elemento_customizado' in estado_anterior:
                elementos_atuais = d.find_elements(By.XPATH, "//div[contains(@class,'sc-eldPxv')]")  # Ajuste o XPath se necessário
                html_atual = ''.join([el.get_attribute('outerHTML') for el in elementos_atuais])
                quantidade_atual = len(elementos_atuais)
                
                # Mudou a quantidade OU o conteúdo dos elementos
                if (quantidade_atual != estado_anterior['quantidade_elementos'] 
                    or html_atual != estado_anterior['elemento_customizado']):
                    return True
            
            return False
        
        WebDriverWait(driver, timeout).until(verificar_condicoes)
        print("✅ Alguma ação foi disparada.")
        return True
    except TimeoutException:
        print("⚠️ Nenhuma mudança detectada.")
        return False

def baixar_imagem_aleatoria():

    # ==================================================
    #            AUTORIA: DIONE BRAGA
    # ==================================================

    url_imagem = "https://picsum.photos/200"
    resposta = requests.get(url_imagem)
    caminho_imagem = os.path.join(os.getcwd(), "imagem_aleatoria.jpg")
    with open(caminho_imagem, 'wb') as file:
        file.write(resposta.content)
    if os.path.exists(caminho_imagem):
        print("Imagem baixada com sucesso.")
        return caminho_imagem
    else:
        print("A imagem não pôde ser baixada.")