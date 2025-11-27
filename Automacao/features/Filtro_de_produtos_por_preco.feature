#language: pt
Funcionalidade: Filtro de produtos por preço
    Cenario: O sistema deve permitir filtragem de produtos por preço
        Dado que o usuário está na página de /products
        Quando clicar em uma valor no menu de filtragem
        Então a página exibirá apenas os produtos com um valor igual ou abaixo ao valor selecionado
