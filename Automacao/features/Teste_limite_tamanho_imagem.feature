# language: pt

Funcionalidade: Teste de limite de tamanho de imagem

  Cenario: Descobrir o tamanho máximo aceito para imagem de produto
    Dado que o usuário está na página de /products
    Quando testar cadastro com imagens de tamanhos crescentes
    Então deve identificar o limite máximo aceito pelo sistema
