# Web Server Gateway Interface
from werkzeug.wrappers import Request, Response
import json


# Classe middleware
class Middleware:

    # Recebe por parâmetro o app, user e password do middleware
    def __init__(self, user, password, app):
        self.app = app
        self.username = user
        self.password = password

    # Função de chamada
    def __call__(self, environ, start_response):

        request = Request(environ)
        username = request.authorization['username']
        password = request.authorization['password']

        # Verifica as credenciais de login no ambiente e compara com as vindas no parâmetro __init__
        if username == self.username and password == self.password:
            environ['user'] = {
                'name': "test"
            }
            return self.app(environ, start_response)

        # Gera response indicando falha nas credenciais
        res = geraResponse(401, "login", {}, "Login falhou")
        return res(environ, start_response)


# Retorna um response
def geraResponse(status, nomeConteudo, conteudo, mensagem=False):
    body = {nomeConteudo: conteudo}

    if mensagem:
        body["Mensagem"] = mensagem

    return Response(json.dumps(body), status, mimetype="application/json")
