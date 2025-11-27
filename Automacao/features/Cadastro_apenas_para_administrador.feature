#language: pt
Funcionalidade: Cadastrar usuario via api
    Cenario: Criando o usuário falso usando faker
        Dado que o usuário deseja realizar cadastro via api
        Quando chamar o método post no endpoint /login e passando os parametros de email e senha
        Então receberá um token para validar o cadastro do usuário
    
    Cenario: Testando login falso
        Dado que o usuário está na página de login
        Quando o usuario preencher com os dados falsos
        Então receberá a mensagem de login com sucesso