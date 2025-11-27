#language: pt
Funcionalidade: Impedir cadastro de usuário externo
    Cenario: O sistema não deve permitir cadastro de usuário externo
        Dado que o usuário está na página de login
        Quando ele acessar a página de cadastro
        E tentar criar conta
        Então receberá a mensagem de cadastrado com sucesso
