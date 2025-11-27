# Script para gerar relatórios de testes Behave
# Executa os testes e gera relatórios em múltiplos formatos

import subprocess
import os
import json
import pandas as pd
from datetime import datetime

# Cores para output no terminal
VERDE = '\033[92m'
AMARELO = '\033[93m'
VERMELHO = '\033[91m'
RESET = '\033[0m'

print(f"{AMARELO}{'='*60}")
print("EXECUTANDO TESTES BEHAVE")
print(f"{'='*60}{RESET}\n")

# Timestamp para nomear os arquivos
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Obtém o diretório do script (pasta Automacao)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Cria pasta reports se não existir
reports_dir = os.path.join(script_dir, 'reports')
os.makedirs(reports_dir, exist_ok=True)

# Caminhos absolutos para os relatórios
json_report = os.path.join(reports_dir, f'relatorio_{timestamp}.json')
txt_report = os.path.join(reports_dir, f'relatorio_{timestamp}.txt')

# ============================================================================
# ORDEM DOS TESTES - Testes listados aqui executam primeiro (na ordem)
# Testes não listados executam depois (em ordem alfabética)
# Comente (#) os testes que não quer executar
# ============================================================================
features_prioritarias = [
    'features/Impedir_cadastro_de_usuario_externo.feature',
    'features/Cadastro_apenas_para_administrador.feature',
    'features/Login_com_email_e_senha.feature',
    'features/Erro_de_login_social.feature',
    'features/Cadastro_de_produtos.feature',
    'features/Cadastro_massa_de_produtos.feature',
    'features/Teste_limite_tamanho_imagem.feature',
    'features/Edicao_de_produtos_cadastrados.feature',
    'features/Exclusao_de_produtos_cadastrados.feature',
    'features/Filtro_de_produtos_por_categoria.feature',
    'features/Filtro_de_produtos_por_preco.feature',
    'features/Atualizacao_automatica.feature',  # Corrigido: features/ com 's'
]

# Descobre todos os arquivos .feature na pasta features
features_dir = os.path.join(script_dir, 'features')
todos_features = []
if os.path.exists(features_dir):
    for arquivo in sorted(os.listdir(features_dir)):
        if arquivo.endswith('.feature'):
            caminho_relativo = f'features/{arquivo}'
            todos_features.append(caminho_relativo)

# Remove comentários da lista prioritária
features_prioritarias_ativas = [f for f in features_prioritarias if not f.strip().startswith('#')]

# Adiciona features que não estão na lista prioritária
features_restantes = [f for f in todos_features if f not in features_prioritarias_ativas]

# Lista final: prioritárias primeiro, depois as restantes
features_ordenadas = features_prioritarias_ativas + features_restantes

print(f"{AMARELO}📋 Ordem de execução dos testes:{RESET}")
for idx, feature in enumerate(features_ordenadas, 1):
    marcador = "⭐" if feature in features_prioritarias_ativas else "  "
    print(f"   {marcador} {idx}. {feature}")
print()

# Comando para executar behave com múltiplos formatos
comando = [
    'behave',
    *features_ordenadas,  # Adiciona os features na ordem especificada
    f'--format=json.pretty',
    f'--outfile={json_report}',
    '--format=pretty',
    f'--outfile={txt_report}',
    '--no-capture',  # Mostra prints durante execução
    '--no-skipped',  # Não mostra steps pulados
    '--show-source'  # Mostra o arquivo fonte de cada step
]

print(f"🔍 Debug - Comando: {' '.join(comando)}\n")
print(f"🔍 Debug - Diretório de execução: {script_dir}\n")

# Executa os testes uma única vez gerando os relatórios
print(f"{AMARELO}{'='*60}")
print("🚀 INICIANDO EXECUÇÃO DOS TESTES")
print(f"{'='*60}{RESET}\n")

# Executa behave uma única vez com geração de relatórios
resultado = subprocess.run(comando, cwd=script_dir, capture_output=False)

print(f"\n{AMARELO}{'='*60}")
if resultado.returncode == 0:
    print(f"{VERDE}✅ Todos os testes passaram!")
else:
    print(f"{VERMELHO}⚠️  Alguns testes falharam")
print(f"{'='*60}{RESET}\n")

print(f"\n{AMARELO}{'='*60}")
if resultado.returncode == 0:
    print(f"{VERDE}✅ TESTES CONCLUÍDOS COM SUCESSO!")
else:
    print(f"{VERMELHO}❌ ALGUNS TESTES FALHARAM!")

print(f"{AMARELO}{'='*60}{RESET}")
print(f"\n📊 Relatórios gerados:")
print(f"   • JSON: {json_report}")
print(f"   • TXT: {txt_report}")

# Verifica se os arquivos foram criados
print(f"\n✓ Verificando arquivos gerados:")
if os.path.exists(json_report):
    tamanho = os.path.getsize(json_report)
    print(f"   {VERDE}✅ JSON: {json_report} ({tamanho} bytes){RESET}")
else:
    print(f"   {VERMELHO}❌ JSON não foi criado{RESET}")

if os.path.exists(txt_report):
    tamanho = os.path.getsize(txt_report)
    print(f"   {VERDE}✅ TXT: {txt_report} ({tamanho} bytes){RESET}")
else:
    print(f"   {VERMELHO}❌ TXT não foi criado{RESET}")

# Gera relatório Excel/CSV a partir do JSON
if os.path.exists(json_report):
    tamanho_json = os.path.getsize(json_report)
    
    if tamanho_json == 0:
        print(f"\n{VERMELHO}⚠️  Arquivo JSON está vazio - não é possível gerar Excel/CSV{RESET}")
        print(f"   Isso pode acontecer quando há erros críticos nos testes.")
        print(f"   Verifique o arquivo TXT para mais detalhes: {txt_report}")
    else:
        print(f"\n{AMARELO}📊 Gerando relatório Excel/CSV...{RESET}")
        
        try:
            # Lê o JSON do Behave
            with open(json_report, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Lista para armazenar dados do resumo
            resumo_funcionalidades = []
            detalhes_steps = []
            
            # Processa cada feature
            for feature in dados:
                feature_nome = feature.get('name', 'Sem nome')
                feature_arquivo = feature.get('location', 'Desconhecido').split(':')[0]
                
                cenarios_total = len(feature.get('elements', []))
                cenarios_passou = 0
                cenarios_falhou = 0
                
                # Processa cada cenário
                for cenario in feature.get('elements', []):
                    if cenario.get('type') != 'scenario':
                        continue
                        
                    cenario_nome = cenario.get('name', 'Sem nome')
                    steps = cenario.get('steps', [])
                    cenario_passou_flag = all(step.get('result', {}).get('status') == 'passed' for step in steps)
                    
                    if cenario_passou_flag:
                        cenarios_passou += 1
                    else:
                        cenarios_falhou += 1
                    
                    # Processa cada step
                    for step in steps:
                        keyword = step.get('keyword', '').strip()
                        texto = step.get('name', '')
                        status = step.get('result', {}).get('status', 'undefined')
                        duracao = step.get('result', {}).get('duration', 0)
                        
                        detalhes_steps.append({
                            'Funcionalidade': feature_nome,
                            'Arquivo': feature_arquivo,
                            'Cenário': cenario_nome,
                            'Step': f"{keyword} {texto}",
                            'Keyword': keyword,
                            'Texto': texto,
                            'Status': status,
                            'Duração (s)': round(duracao, 2) if duracao else 0
                        })
                
                # Adiciona ao resumo
                resumo_funcionalidades.append({
                    'Funcionalidade': feature_nome,
                    'Arquivo': feature_arquivo,
                    'Total Cenários': cenarios_total,
                    'Passou': cenarios_passou,
                    'Falhou': cenarios_falhou,
                    'Taxa Sucesso (%)': round((cenarios_passou / cenarios_total * 100) if cenarios_total > 0 else 0, 1)
                })
            
            # Cria DataFrames
            df_resumo = pd.DataFrame(resumo_funcionalidades)
            df_detalhes = pd.DataFrame(detalhes_steps)
            
            # Define nome dos arquivos
            excel_file = json_report.replace('.json', '_relatorio.xlsx')
            csv_file = json_report.replace('.json', '_resumo.csv')
            
            # Salva em Excel com múltiplas abas
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
                df_detalhes.to_excel(writer, sheet_name='Detalhes dos Steps', index=False)
            
            # Salva CSV apenas do resumo
            df_resumo.to_csv(csv_file, index=False, encoding='utf-8-sig')
            
            print(f"   {VERDE}✅ EXCEL: {excel_file}{RESET}")
            print(f"   {VERDE}✅ CSV: {csv_file}{RESET}")
            
            # Exibe resumo no terminal
            print(f"\n{AMARELO}{'='*70}")
            print("📊 RESUMO DOS TESTES")
            print(f"{'='*70}{RESET}")
            print(df_resumo.to_string(index=False))
            print(f"{AMARELO}{'='*70}{RESET}")
            
            # Totais gerais
            total_cenarios = df_resumo['Total Cenários'].sum()
            total_passou = df_resumo['Passou'].sum()
            total_falhou = df_resumo['Falhou'].sum()
            
            print(f"\n📈 TOTAIS GERAIS:")
            print(f"   ✅ Passou: {total_passou}/{total_cenarios}")
            print(f"   ❌ Falhou: {total_falhou}/{total_cenarios}")
            print(f"   📊 Taxa de Sucesso: {round((total_passou/total_cenarios*100) if total_cenarios > 0 else 0, 1)}%")
            
        except Exception as e:
            print(f"   {VERMELHO}❌ Erro ao gerar Excel/CSV: {e}{RESET}")
else:
    print(f"\n{VERMELHO}❌ Arquivo JSON não foi criado - não é possível gerar relatórios{RESET}")

print(f"\n")
