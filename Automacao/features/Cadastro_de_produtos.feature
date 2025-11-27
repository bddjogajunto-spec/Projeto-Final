#language: pt
Funcionalidade: Cadastro de produtos
    Cenario: O sistema deve permitir cadastro de produtos
        Dado que o usuário está na página de /products
        Quando clicar no botão adicionar
        E preencher todos os dados obrigatórios
        E clicar em enviar novo o produto
        Então deve receber a mensagem de novo produto criado com sucesso
