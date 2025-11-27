#language: pt

Funcionalidade: Login com rede social
    Cenario: Tentar fazer login social com Google
        Dado que o usuário está na página de login
        Quando clica no Entrar com "Google"
        Então recebe erro de email não digitado para login

    Cenario: Tentar fazer login social com Facebook
        Dado que o usuário está na página de login
        Quando clica no Entrar com "Facebook"
        Então recebe erro de email não digitado para login