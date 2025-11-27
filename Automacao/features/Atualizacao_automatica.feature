#language: pt
Funcionalidade: Atualização automática
    Cenario: O sistema deve atualizar automaticamente a quantidade de produtos disponíveis após cada transação (compras, vendas, devoluções).
        Dado que o usuário está na página de /products
        Quando o estoque mudar 
        Então o site deve atualizar a informação automaticamente
