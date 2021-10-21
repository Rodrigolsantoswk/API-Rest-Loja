from flask import Flask, request, Response
import json
from sqlalchemy.orm import aliased
from flask_sqlalchemy import get_debug_queries
from dbconfig import db, app
from datetime import datetime
from categoria import categoria


# Retorna um response
def geraResponse(status, nomeConteudo, conteudo, mensagem=False):
    body = {nomeConteudo: conteudo}

    if mensagem:  # Se mensagem não está na chamada, então não envia mensagem no corpo do JSON
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status, mimetype="application/json")


@app.route("/categoria", methods=["GET"])
def selecionaCategorias():
    # Requisita o middleware para acessar a rota
    request.environ['user']

    body = []

    # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
    categoriaObj = categoria.query.all()
    try:
        for Category in categoriaObj:  # Para cada objeto na lista, insere em Body o objeto.toJson()
            body.append(Category.toJson())

        return geraResponse(200, "Categoria", body, "Ok")
    except Exception as e:
        print("Categoria: " + str(e))
        return geraResponse(400, "Categoria", body, "Erro ao selecionar categorias")


@app.route("/categoria", methods=["POST"])
def InserirCategoria():
    body = request.get_json()  # Requisita o body na requisição

    if body is None:  # Se o body estiver vazio ou não existir, então retorna response
        return geraResponse(400, "categoria", {}, "Sem o JSON")

    try:
        if 'nomeCategoria' not in body:  # Se parâmetro requisitado não estiver em body, então gera response
            return geraResponse(400, "categoria", {}, "nomeCategoria não está no JSON")

        nomeCategoria = body['nomeCategoria']

        # Seleciona categoria e filtra por nomeCategoria para verificar se não existe antes de criar
        categoriaObj = categoria.query.filter_by(nomeCategoria=nomeCategoria).first()
        print(categoriaObj)

        if categoriaObj is None:  # Se categoria não retornar nada, então cria um objeto categoria e
            categoriaObj = categoria(nomeCategoria=nomeCategoria)

            db.session.add(categoriaObj)  # Insere no banco de dados
            db.session.commit()  # Realiza Commit
            return geraResponse(201, "categoria", categoriaObj.toJson(), "Objeto inserido com sucesso")
        else:
            # Esta resposta será enviada quando uma requisição conflitar com o estado atual do servidor.
            return geraResponse(409, "categoria", {}, "Categoria já existe")
    except Exception as e:
        print(e)
        return geraResponse(400, "categoria", {}, "Erro ao inserir Categoria")  # 400 Bad Request


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
