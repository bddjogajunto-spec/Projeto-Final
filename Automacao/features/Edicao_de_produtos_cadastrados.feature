#language: pt
Funcionalidade: Edição de produtos cadastrados
    Cenario: O sistema deve permitir edição de produtos cadastrados
        Dado que o usuário está na página de /products
        E abrir a página do produto desejado
        Quando editar as informações
        E clicar em salvar alterações
        Então receberá a mensagem de produto atualizado com sucesso
