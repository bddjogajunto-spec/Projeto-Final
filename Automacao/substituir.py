import os
import unicodedata
import pyperclip # serve para escrever a área de transferencia

def remover_acentos(texto):
    # Normaliza o texto
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Remove os caracteres de acento
    texto_sem_acento = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sem_acento

texto = input('cole o texto... ')
under = remover_acentos(texto)
under = under.replace(' ', '_')
requisito = input('cole o requisito... ')

caminho_atual = os.path.dirname(__file__)
features = os.path.join(caminho_atual, 'features', f'{under}.feature')

steps = os.path.join(caminho_atual, 'features', 'steps', f'step_{under}.py')

language = '#language: pt\n'

cenario = input('cole o cenario... ')
print('Apenas copie o caso, volte ao terminal e dê enter\n')
input()
caso = pyperclip.paste()

caso = caso.strip('"').strip("'")
caso = caso.replace('DADO', 'Dado').replace('QUANDO', 'Quando').replace('ENTÃO', 'Então')

# Adiciona indentação de 8 espaços em cada linha do caso
linhas_caso = caso.split('\n')
caso_identado = '\n'.join('        ' + linha for linha in linhas_caso)

escrita = [language, str(f'Funcionalidade: {texto}\n'), str(f'    Cenario: {cenario}\n'), str(f'{caso_identado}\n')]

with open(features, 'w', encoding='utf-8') as arquivo:
    for i in escrita:
        arquivo.write(i)

caminho_base = os.path.join(os.path.dirname(caminho_atual), 'base.py')
with open(caminho_base, 'r', encoding='utf-8') as arquivo_imports:
    conteudo_base = arquivo_imports.read()

bdd = {
    'Dado' : '@given',
    'Quando' : '@when',
    'Então' : '@then'
}

with open(steps, 'w', encoding='utf-8') as arquivo:
    arquivo.write(f'{conteudo_base}\n\n')
    decorador_atual = '@given'  # Guarda o último decorador usado
    
    for linha in linhas_caso:
        linha_limpa = linha.strip()
        if not linha_limpa:  # Pula linhas vazias
            continue
            
        # Verifica qual palavra-chave BDD está na linha
        decorador_encontrado = False
        for key, decorador in bdd.items():
            if linha_limpa.startswith(key):
                decorador_atual = decorador
                decorador_encontrado = True
                # Remove apenas a palavra-chave BDD do início
                texto_sem_bdd = linha_limpa[len(key):].strip()
                arquivo.write(f'{decorador}("{texto_sem_bdd}")\n')
                arquivo.write(f'def step_impl(context):\n')
                arquivo.write(f'    print("{linha_limpa}")\n\n')
                arquivo.write(f'    time.sleep(2)\n\n')
                break
        
        # Se começa com "E", usa o último decorador
        if not decorador_encontrado and linha_limpa.startswith('E '):
            texto_sem_e = linha_limpa[2:].strip()  # Remove "E "
            arquivo.write(f'{decorador_atual}("{texto_sem_e}")\n')
            arquivo.write(f'def step_impl(context):\n')
            arquivo.write(f'    print("{linha_limpa}")\n\n')
            arquivo.write(f'    time.sleep(2)\n\n')
    arquivo.write(f'    print("{requisito}")\n\n')
    arquivo.write('    context.driver.quit()')

print(under)