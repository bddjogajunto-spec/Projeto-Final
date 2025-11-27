# 🎯 Projeto Final - QA Avançado
**Sistema de Automação de Testes com BDD (Behavior Driven Development)**

> Projeto completo de automação de testes para aplicação web de e-commerce usando Behave, Selenium e Python.

---

## 📋 Índice
- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Executando os Testes](#-executando-os-testes)
- [Gerando Novos Testes](#️-gerando-novos-testes)
- [Debugging](#-como-depurar-testes)
- [Padrão de Código](#-padrão-de-prints-nos-testes)
- [Arquivos e Funcionalidades](#-arquivos-e-funcionalidades)

---

## 🎯 Sobre o Projeto

Este projeto implementa **automação de testes E2E (End-to-End)** para uma aplicação web de gerenciamento de produtos. Os testes cobrem:

- ✅ Autenticação (login/logout)
- ✅ Cadastro de usuários e produtos
- ✅ CRUD completo de produtos
- ✅ Filtros e buscas
- ✅ Validações de permissões
- ✅ Testes de limite e validação de dados
- ✅ Integração com API REST

**Aplicação testada**: [https://projetofinal.jogajuntoinstituto.org](https://projetofinal.jogajuntoinstituto.org)  
**API testada**: [https://apipf.jogajuntoinstituto.org](https://apipf.jogajuntoinstituto.org)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição | Versão |
|------------|-----------|--------|
| **Python** | Linguagem de programação | 3.x |
| **Behave** | Framework BDD para Python | 1.3.3 |
| **Selenium** | Automação de navegadores | 4.38.0 |
| **Faker** | Geração de dados falsos | 38.2.0 |
| **Pandas** | Manipulação e análise de dados | 2.3.3 |
| **Pillow** | Geração e manipulação de imagens | 12.0.0 |
| **Requests** | Cliente HTTP para API | 2.32.5 |
| **OpenPyXL** | Geração de relatórios Excel | 3.1.5 |
| **Pyperclip** | Cópia automática para área de transferência | 1.11.0 |
| **Python-dotenv** | Gerenciamento de variáveis de ambiente | 1.2.1 |
| **Webdriver-manager** | Gerenciamento automático de drivers | 4.0.2 |
| **Trio** | Framework assíncrono para Selenium | 0.32.0 |
| **Colorama** | Cores no terminal Windows | 0.4.6 |

---

## 📁 Estrutura do Projeto

```
Projeto_final/
│
├── 📂 Automacao/                    # Pasta principal dos testes
│   ├── 📂 features/                 # Arquivos de teste em BDD (Gherkin)
│   │   ├── *.feature                # Cenários de teste em linguagem natural
│   │   └── 📂 steps/                # Implementação dos steps em Python
│   │       ├── step_comum.py        # Steps compartilhados entre testes
│   │       └── step_*.py            # Steps específicos de cada feature
│   │
│   ├── 📂 utils/                    # Funções utilitárias
│   │   ├── utilitarios.py           # Funções auxiliares (evidências, validações)
│   │   ├── api_functions.py         # Funções para chamadas API REST
│   │   └── user.json                # Credenciais do administrador
│   │
│   ├── 📂 imagem_produto/           # Imagens geradas para testes
│   ├── 📂 evidencia/                # Screenshots dos testes
│   ├── 📂 reports/                  # Relatórios de execução (JSON, TXT, Excel, CSV)
│   │
│   ├── behave.ini                   # Configurações do Behave
│   ├── executar_testes.py           # Script principal de execução
│   └── substituir.py                # Gerador automático de testes
│
├── base.py                          # Template de imports para novos steps
├── teste.py                         # Arquivo de testes/exemplos
├── requirements.txt                 # Dependências do projeto
└── README.md                        # Este arquivo

```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Pré-requisitos
- **Python 3.8+** instalado
- **Microsoft Edge** instalado (ou altere para Chrome/Firefox)
- **Git** (opcional, para clonar o repositório)

### 2️⃣ Clonar o Repositório
```powershell
git clone <URL_DO_SEU_REPOSITORIO>
cd Projeto_final
```

### 3️⃣ Criar Ambiente Virtual
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4️⃣ Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 5️⃣ Configurar Credenciais
Edite o arquivo `Automacao/utils/user.json` com suas credenciais de administrador:
```json
{
    "usuario": "seu_email@admin.com",
    "senha": "sua_senha"
}
```

---

## 🚀 Executando os Testes

### ✅ Método Recomendado: Script Automatizado

```powershell
cd Automacao
python executar_testes.py
```

**O que o script faz:**
- ⭐ Executa testes na ordem de prioridade definida
- 📊 Gera relatórios em **4 formatos** (JSON, TXT, Excel, CSV)
- 🎯 Mostra progresso em tempo real
- 📈 Exibe resumo consolidado ao final
- 🖼️ Captura screenshots automaticamente

### 📋 Ordem de Execução dos Testes

Os testes são executados nesta sequência (definida em `executar_testes.py`):

1. **Impedir_cadastro_de_usuario_externo** - Validar bloqueio de cadastro público
2. **Cadastro_apenas_para_administrador** - Testar cadastro via API + login web ⚠️ **DEVE SER EXECUTADO PRIMEIRO**
3. **Login_com_email_e_senha** - Validar autenticação de admin
4. **Erro_de_login_social** - Testar erro ao usar login social sem email
5. **Cadastro_de_produtos** - Testar cadastro individual de produto
6. **Cadastro_massa_de_produtos** - Testar cadastro em lote (10 produtos)
7. **Teste_limite_tamanho_imagem** - Descobrir limite de tamanho de imagem
8. **Edicao_de_produtos_cadastrados** - Testar edição de produtos
9. **Exclusao_de_produtos_cadastrados** - Testar exclusão de produtos
10. **Filtro_de_produtos_por_categoria** - Validar filtros de categoria
11. **Filtro_de_produtos_por_preco** - Validar filtros de preço
12. **Atualizacao_automatica** - Testar atualização automática de estoque

> ⚠️ **IMPORTANTE:** O teste `Cadastro_apenas_para_administrador` **DEVE ser executado primeiro** pois ele cria o arquivo `utils/user.json` com as credenciais necessárias para os demais testes.
>
> **Testes que dependem do `user.json`:**
> - `Login_com_email_e_senha` (usa `obter_usuario()`)
> - `Cadastro_de_produtos` (usa `obter_usuario()`)
> - Todos os testes que usam `step_comum.py` para login (através do step "Dado que o Usuário possui conta de administrador cadastrada")
>
> Se você executar os testes individualmente, certifique-se de rodar `Cadastro_apenas_para_administrador` primeiro ou crie manualmente o arquivo `utils/user.json`.

### 🔧 Executar Manualmente com Behave

```powershell
cd Automacao

# Rodar todos os testes
behave

# Rodar teste específico
behave features/Cadastro_de_produtos.feature

# Modo verbose (mais detalhes)
behave -v

# Ver prints durante execução
behave --no-capture

# Combinar opções
behave -v --no-capture features/Login_com_email_e_senha.feature
```

---

## 🛠️ Gerando Novos Testes

O script `substituir.py` **automatiza a criação** de novos casos de teste:

### Como usar:

```powershell
cd Automacao
python substituir.py
```

### Passo a passo:

1. **Digite o nome da funcionalidade**  
   Exemplo: `Adicionar ao Carrinho`

2. **Digite o cenário**  
   Exemplo: `Usuário adiciona produto ao carrinho`

3. **Copie o caso de teste do Excel** (formato BDD)  
   ```
   DADO que o usuário está logado
   QUANDO clicar em adicionar ao carrinho
   E visualizar o carrinho
   ENTÃO deve ver o produto adicionado
   ```

4. **Pressione Enter** - O script irá:
   - ✅ Criar arquivo `.feature` com o BDD
   - ✅ Criar arquivo `step_*.py` com os steps
   - ✅ Remover acentos e formatação
   - ✅ Adicionar imports necessários
   - ✅ Estruturar o código automaticamente

**Resultado:**
- `features/Adicionar_ao_Carrinho.feature`
- `features/steps/step_Adicionar_ao_Carrinho.py`

---

## 🔍 Como Depurar Testes

### Método 1: Debugger do VS Code ⭐ (Recomendado)

1. Abra o arquivo `.feature` que deseja depurar
2. Coloque **breakpoints** nos arquivos de steps (clique na margem esquerda)
3. Pressione **F5** ou vá em **Run and Debug** (Ctrl+Shift+D)
4. Selecione:
   - **"Behave: Debug Current Feature"** - Depura o arquivo aberto
   - **"Behave: Debug All Features"** - Depura todos os testes

**Atalhos do Debugger:**
| Tecla | Ação |
|-------|------|
| **F10** | Avançar linha a linha (Step Over) |
| **F11** | Entrar em funções (Step Into) |
| **Shift+F11** | Sair da função (Step Out) |
| **F5** | Continuar até próximo breakpoint |

### Método 2: Python Debugger (pdb)

Adicione no código onde deseja pausar:
```python
import pdb; pdb.set_trace()
```

**Comandos do pdb:**
- `n` (next) - Próxima linha
- `s` (step) - Entrar na função
- `c` (continue) - Continuar execução
- `p variavel` - Imprimir valor
- `l` (list) - Mostrar código
- `q` (quit) - Sair

### Método 3: Prints e Verbose Mode

```powershell
behave --no-capture          # Ver prints durante execução
behave -v                    # Modo verbose
behave -v --no-capture       # Combinar ambos
```

---

## 🎨 Padrão de Prints nos Testes

Todos os testes seguem um **formato visual consistente** com emojis:

### 🎭 Emojis Padronizados:
| Emoji | Significado |
|-------|-------------|
| 🌐 | Carregando páginas / Navegação |
| 🔐 | Login / Autenticação |
| 📝 | Preenchendo formulários |
| 🖼️ | Gerando/manipulando imagens |
| 📦 | Cadastrando produtos |
| 🔍 | Filtros / Buscas |
| 💰 | Preços / Valores monetários |
| ✅ | Sucesso / Passou |
| ❌ | Erro / Falhou |
| ⚠️ | Aviso / Atenção |
| 💬 | Mensagens do sistema |
| 📊 | Relatórios / Estatísticas |

### Formato Visual:
```
────────────────────────────────────────────────────────────
🔍 [1/5] Testando categoria: Eletrônicos
────────────────────────────────────────────────────────────
✅ Filtro aplicado com sucesso
```

### Exemplos de Mensagens:
```python
print("✅ Produto cadastrado com sucesso")
print("❌ Erro ao cadastrar produto")
print("📦 Produto 3/10")
print("🔍 [2/8] Testando faixa de preço: R$ 50 - R$ 100")
```

---

## 📚 Arquivos e Funcionalidades

### 🔧 Arquivos de Configuração

#### `behave.ini`
Configuração do framework Behave:
```ini
[behave]
format = json, pretty               # Formatos de saída
outfiles = reports/relatorio.json   # Arquivos de relatório
paths = features                    # Caminho dos testes
show_skipped = false                # Ocultar steps pulados
```

#### `requirements.txt`
Lista todas as dependências do projeto com versões específicas. Instale com:
```powershell
pip install -r requirements.txt
```

### 🐍 Scripts Python

#### `executar_testes.py`
**Script principal de execução dos testes**. Funcionalidades:
- Executa testes em ordem customizada (lista prioritária)
- Gera relatórios em 4 formatos (JSON, TXT, Excel, CSV)
- Exibe progresso em tempo real com cores
- Calcula estatísticas (taxa de sucesso, tempo, etc.)
- Cria pasta `reports/` automaticamente

**Como usar:**
```powershell
cd Automacao
python executar_testes.py
```

#### `substituir.py`
**Gerador automático de casos de teste**. Funcionalidades:
- Remove acentos dos nomes de arquivo
- Converte BDD (DADO/QUANDO/ENTÃO) para formato Behave
- Cria arquivo `.feature` e `step_*.py` simultaneamente
- Adiciona imports base automaticamente
- Usa `pyperclip` para copiar do Excel

**Como usar:**
```powershell
cd Automacao
python substituir.py
```

#### `base.py`
**Template de imports** usado pelo `substituir.py`. Contém:
- Imports do Behave (given, when, then)
- Imports do Selenium (WebDriver, By, Keys, etc.)
- Imports de bibliotecas auxiliares (time, faker, pandas, etc.)
- Configuração inicial do Edge

### 🧰 Pasta `utils/`

#### `utilitarios.py`
**Funções auxiliares compartilhadas**:

| Função | Descrição |
|--------|-----------|
| `evidencia()` | Captura screenshot e salva em `evidencia/` |
| `obter_usuario()` | Lê credenciais do `user.json` |
| `gerar_imagem_com_tamanho()` | Gera JPEG com tamanho específico (MB) |
| `capturar_estado()` | Captura URL, dialogs, HTML da página |
| `verificar_mudanca()` | Verifica se houve mudança após ação |
| `baixar_imagem_aleatoria()` | Baixa imagem aleatória de API |

**Exemplo de uso:**
```python
# Capturar evidência
evidencia(context, 'nome_do_teste')

# Gerar imagem de 1.2MB
imagem, tamanho = gerar_imagem_com_tamanho(1.2, 'produto_teste')

# Verificar mudança na página
estado_antes = capturar_estado(driver)
botao.click()
mudou = verificar_mudanca(driver, estado_antes)
```

#### `api_functions.py`
**Funções para interação com a API REST**:

| Função | Endpoint | Método | Descrição |
|--------|----------|--------|-----------|
| `login()` | `/login` | POST | Autentica usuário e retorna token |
| `register()` | `/register` | POST | Cadastra novo usuário |
| `cadastro()` | `/` | POST | Cadastra produto com imagem |
| `listar_produtos()` | `/` | GET | Lista todos os produtos |
| `deletar_produto()` | `/{id}` | DELETE | Exclui produto por ID |

**Exemplo de uso:**
```python
# Login via API
dados = {'email': 'admin@test.com', 'password': '123'}
resposta = login(dados)
token = resposta['token']

# Autenticação
headers = {'Authorization': f'Bearer {token}'}

# Listar produtos
produtos = listar_produtos(headers)
```

#### `user.json`
Arquivo JSON com credenciais do administrador:
```json
{
    "usuario": "bdd@admin.com",
    "senha": "admin123"
}
```

### 📝 Arquivos de Teste (.feature)

Localizados em `Automacao/features/`, escritos em **Gherkin (BDD)**:

| Arquivo | Requisito | Descrição |
|---------|-----------|-----------|
| `Impedir_cadastro_de_usuario_externo.feature` | RF0001 | Valida que usuários não conseguem se registrar |
| `Cadastro_apenas_para_administrador.feature` | RF0003 | Testa cadastro via API + login web |
| `Login_com_email_e_senha.feature` | RF0002 | Valida autenticação de administrador |
| `Erro_de_login_social.feature` | NF0004 | Testa erro ao usar login Google/GitHub sem email |
| `Cadastro_de_produtos.feature` | RF0004 | Cadastra produto individual com imagem |
| `Cadastro_massa_de_produtos.feature` | RF0004 | Cadastra 10 produtos em sequência |
| `Teste_limite_tamanho_imagem.feature` | NF0001 | Descobre limite de tamanho de imagem |
| `Edicao_de_produtos_cadastrados.feature` | RF0005 | Edita informações de produto |
| `Exclusao_de_produtos_cadastrados.feature` | RF0008 | Exclui produtos cadastrados |
| `Filtro_de_produtos_por_categoria.feature` | RF0006 | Valida filtros de categoria |
| `Filtro_de_produtos_por_preco.feature` | RF0007 | Valida filtros de faixa de preço |
| `Atualizacao_automatica.feature` | RF0010 | Testa atualização automática de estoque |

### 🔍 Pasta `steps/`

Contém a **implementação em Python** de cada step BDD:

- **`step_comum.py`**: Steps compartilhados (login, navegação)
- **`step_*.py`**: Implementação específica de cada feature

---

## 📊 Relatórios Gerados

Após executar `executar_testes.py`, são gerados automaticamente na pasta `reports/`:

| Formato | Arquivo | Descrição |
|---------|---------|-----------|
| **JSON** | `relatorio_YYYYMMDD_HHMMSS.json` | Dados estruturados para processamento |
| **TXT** | `relatorio_YYYYMMDD_HHMMSS.txt` | Relatório legível com detalhes |
| **Excel** | `relatorio_YYYYMMDD_HHMMSS_relatorio.xlsx` | Planilha com 2 abas (Resumo + Detalhes) |
| **CSV** | `relatorio_YYYYMMDD_HHMMSS_resumo.csv` | Resumo em CSV para análise |

**Exemplo de Resumo Exibido:**
```
════════════════════════════════════════════════════════════════════
📊 RESUMO DOS TESTES
════════════════════════════════════════════════════════════════════
Funcionalidade                        Total  Passou  Falhou  Taxa (%)
─────────────────────────────────────────────────────────────────────
Login com email e senha                  1       1       0     100.0
Cadastro de produtos                     1       1       0     100.0
Filtro por categoria                     1       0       1       0.0
════════════════════════════════════════════════════════════════════

📈 TOTAIS GERAIS:
   ✅ Passou: 2/3
   ❌ Falhou: 1/3
   📊 Taxa de Sucesso: 66.7%
```

---

## 🎓 Conceitos e Padrões Utilizados

### BDD (Behavior Driven Development)
Testes escritos em **linguagem natural** (Gherkin):
```gherkin
Dado que o usuário está na página de login
Quando preencher email e senha válidos
Então deve ser redirecionado para /products
```

### Page Object Pattern (Implícito)
Elementos são organizados em dicionários:
```python
login = {
    'email': driver.find_element(By.NAME, 'email'),
    'senha': driver.find_element(By.NAME, 'password'),
    'botao': driver.find_element(By.XPATH, '//button')
}
```

### Data-Driven Testing
Usa **Faker** para gerar dados aleatórios:
```python
from faker import Faker
fake = Faker()
nome = fake.name()
email = fake.email()
```

### Evidências Automatizadas
Captura screenshots em pontos críticos:
```python
evidencia(context, 'Cadastro_produto_sucesso')
```

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de **QA Avançado** do **Instituto Joga Junto**.

---

## 👥 Squad

**Equipe de Desenvolvimento e QA:**  
Repositório do Squad: [GitHub Squad](https://github.com/<USUARIO_SQUAD>/<REPOSITORIO_SQUAD>)

---

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório!**
