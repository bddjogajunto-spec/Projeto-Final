# ============================================================================
# ARQUIVO: step_Teste_limite_tamanho_imagem.py
# PROPÓSITO: Descobrir o limite máximo de tamanho de imagem aceito pelo sistema
# CENÁRIO: Testa cadastro com imagens de 0.5MB até 1.5MB em incrementos de 0.1MB
# ============================================================================

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker as fk
from utils.utilitarios import evidencia, gerar_imagem_com_tamanho

fake = fk()

@when("testar cadastro com imagens de tamanhos crescentes")
def step_impl(context):
    """Testa cadastro de produtos com imagens de tamanhos crescentes.
    Começa em 0.5MB e vai até 1.5MB em incrementos de 0.1MB.
    Para quando encontra o primeiro erro.
    """
    
    # Lista de tamanhos para testar (em MB)
    tamanhos_teste = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    
    # Dicionário para armazenar resultados
    resultados = {
        'sucesso': [],
        'falhou': []
    }
    
    print(f"\n{'='*70}")
    print("🔍 INICIANDO TESTE DE LIMITE DE TAMANHO DE IMAGEM")
    print(f"{'='*70}\n")
    
    # Abre o modal ANTES do loop
    try:
        botao = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/header/button')
        botao.click()
        time.sleep(2)
        print("✅ Modal aberto - Iniciando testes")
    except Exception as e:
        print(f"❌ Erro ao abrir modal inicial: {e}")
        context.resultados_limite = resultados
        return
    
    for tamanho_alvo in tamanhos_teste:
        print(f"\n{'─'*70}")
        print(f"📊 Testando imagem de {tamanho_alvo} MB")
        print(f"{'─'*70}")
        
        # Verifica se o modal está aberto (pode ter fechado por algum motivo)
        modal_presente = context.driver.find_elements(By.XPATH, "//div[@role='dialog' and @data-state='open']")
        
        if not modal_presente:
            print(f"⚠️ Modal fechou - Reabrindo...")
            try:
                botao = context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/header/button')
                botao.click()
                time.sleep(2)
            except Exception as e:
                print(f"❌ Erro ao reabrir modal: {e}")
                break
        else:
            print("✅ Modal já está aberto")
        
        # Gera dados aleatórios
        nome = f"Teste_{tamanho_alvo}MB_{fake.word()}"
        
        try:
            print(f"\n🖼️  Gerando imagem de {tamanho_alvo} MB...")
            imagem, tamanho_real = gerar_imagem_com_tamanho(tamanho_alvo, nome)
            
            # Localiza campos do formulário
            form = {
                'nome': context.driver.find_element(By.NAME, 'name'),
                'description': context.driver.find_element(By.NAME, 'description'),
                'categoria': context.driver.find_elements(By.XPATH, "//div[contains(@class,'sc-dAbbOL')]//label"),
                'preco': context.driver.find_element(By.NAME, 'price'),
                'imagem': context.driver.find_element(By.NAME, 'image'),
                'frete': context.driver.find_element(By.NAME, 'shipment'),
            }
            
            # Preenche formulário
            form['nome'].send_keys(nome)
            form['description'].send_keys(f'Teste de limite {tamanho_alvo}MB')
            form['categoria'][0].click()
            form['preco'].send_keys(str(fake.random_int(10, 100)))
            form['imagem'].send_keys(imagem)
            form['frete'].send_keys(str(fake.random_int(5, 20)))
            
            time.sleep(1)
            
            # Envia o formulário
            context.driver.find_element(By.XPATH, '/html/body/div[1]/header/section[2]/div/div[1]/div/form/button').click()
            
            # Aguarda resposta (toast)
            wait = WebDriverWait(context.driver, 10)
            toast = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@role='status' and (contains(text(),'sucesso') or contains(text(),'Erro') or contains(text(),'erro'))]"
                ))
            )
            
            mensagem = toast.text.strip()
            
            # Verifica resultado
            if "sucesso" in mensagem.lower():
                print(f"✅ Aceita: {tamanho_real:.2f} MB")
                resultados['sucesso'].append({
                    'tamanho_alvo': tamanho_alvo,
                    'tamanho_real': tamanho_real,
                    'mensagem': mensagem
                })
            else:
                print(f"❌ Rejeitada: {tamanho_real:.2f} MB")
                print(f"   💬 {mensagem}")
                evidencia(context, f'Limite_FALHA_{tamanho_alvo}MB')
                resultados['falhou'].append({
                    'tamanho_alvo': tamanho_alvo,
                    'tamanho_real': tamanho_real,
                    'mensagem': mensagem
                })
                # Para no primeiro erro
                break
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ ERRO durante teste: {e}")
            evidencia(context, f'Limite_ERRO_{tamanho_alvo}MB')
            resultados['falhou'].append({
                'tamanho_alvo': tamanho_alvo,
                'tamanho_real': 0,
                'mensagem': str(e)
            })
            break
    
    # Salva resultados no context
    context.resultados_limite = resultados


@then("deve identificar o limite máximo aceito pelo sistema")
def step_impl(context):
    """Exibe relatório final dos testes de limite de tamanho."""
    
    resultados = context.resultados_limite
    
    print(f"\n{'='*70}")
    print("📊 RELATÓRIO FINAL - TESTE DE LIMITE DE TAMANHO")
    print(f"{'='*70}\n")
    
    maior_aceito = None
    
    if resultados['sucesso']:
        print(f"✅ IMAGENS ACEITAS ({len(resultados['sucesso'])}):")
        for resultado in resultados['sucesso']:
            print(f"   • {resultado['tamanho_real']:.2f} MB (alvo: {resultado['tamanho_alvo']} MB)")
        
        maior_aceito = max(r['tamanho_real'] for r in resultados['sucesso'])
        print(f"\n🎯 MAIOR TAMANHO ACEITO: {maior_aceito:.2f} MB")
    
    if resultados['falhou']:
        print(f"\n❌ IMAGENS REJEITADAS ({len(resultados['falhou'])}):")
        for resultado in resultados['falhou']:
            if resultado['tamanho_real'] > 0:
                print(f"   • {resultado['tamanho_real']:.2f} MB (alvo: {resultado['tamanho_alvo']} MB)")
                print(f"     Motivo: {resultado['mensagem']}")
        
        if maior_aceito is not None and resultados['falhou'][0]['tamanho_real'] > 0:
            print(f"\n⚠️  LIMITE IDENTIFICADO: Entre {maior_aceito:.2f} MB e {resultados['falhou'][0]['tamanho_real']:.2f} MB")
        elif maior_aceito is None:
            print(f"\n⚠️  NENHUMA IMAGEM FOI ACEITA - Todas foram rejeitadas desde {resultados['falhou'][0]['tamanho_alvo']} MB")
    
    print(f"\n{'='*70}\n")
    
    # Captura evidência final
    evidencia(context, 'Teste_limite_FINAL')
    
    print("Requisito que inspirou este teste: NF0001\n")
    
    time.sleep(2)
    context.driver.quit()
