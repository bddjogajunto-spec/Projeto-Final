#language: pt
Funcionalidade: Filtro de produtos por categoria
    Cenario: O sistema deve permitir filtragem de produtos por categoria
        Dado que o usuário está na página de /products
        Quando clicar em uma categoria no menu de filtragem
        Então a página exibirá apenas os produtos dessa categoria
