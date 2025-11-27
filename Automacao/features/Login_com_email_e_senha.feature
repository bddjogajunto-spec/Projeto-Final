#language: pt
Funcionalidade: Login com email e senha
    Cenario: O sistema deva permitir login com e-mail e senha
        Dado que o Usuário possui conta de administrador cadastrada
        Quando tentar logar com seu email e senha
        Então deverá ser redirecionado para a página de cadastro de produtos
