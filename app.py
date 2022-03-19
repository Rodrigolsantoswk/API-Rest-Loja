from flask import Flask, request, Response
import json
from sqlalchemy.orm import aliased
from pprint import pprint
from flask_sqlalchemy import get_debug_queries
from dbconfig import db, app
from datetime import datetime
from caixa import caixa
from marca import marca
from categoria import categoria
from produto import produto


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


@app.route("/categoria/<nomeCategoria>", methods=["DELETE"])
def deleteCategoria(nomeCategoria):
    request.environ['user']

    categoriaObj = categoria.query.filter_by(nomeCategoria=nomeCategoria).first()

    try:
        db.session.delete(categoriaObj)
        db.session.commit()
        return geraResponse(200, "categoria", categoriaObj.toJson(), "Categoria deletada")
    except Exception as e:
        print(e)
        return geraResponse(400, "categoria", {}, "Erro ao deletar a categoria")


@app.route("/caixa", methods=["GET"])
def selecionaCaixas():
    # Requisita o middleware para acessar a rota
    request.environ['user']

    body = []

    # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
    caixaObj = caixa.query.all()
    try:
        for i in caixaObj:
            body.append(i.toJson())
        return geraResponse(200, "Caixa", body, "Ok")
    except Exception as e:
        print("Caixa: " + str(e))
        return geraResponse(400, "Caixa", {}, "Erro ao selecionar Caixas")


@app.route("/caixa", methods=["POST"])
def InserirCaixa():
    body = request.get_json()  # Requisita o body na requisição

    if body is None:  # Se o body estiver vazio ou não existir, então retorna response
        return geraResponse(400, "Caixa", {}, "Sem o JSON")

    try:
        for i in ['nome', 'dataNascimento']:
            if i not in body:
                return geraResponse(400, "Caixa", {}, "without: " + i)

        nome = body['nome']
        dataNascimento = body['dataNascimento']
        now = datetime.now()
        caixaObj = caixa(nomeCaixa=nome, dataNascimentoCaixa=dataNascimento, inseridoEm=now)

        db.session.add(caixaObj)  # Insere no banco de dados
        db.session.commit()  # Realiza Commit
        return geraResponse(201, "Caixa", caixaObj.toJson(), "Caixa inserido com sucesso")
    except Exception as e:
        print(e)
        return geraResponse(400, "Caixa", {}, "Erro ao inserir Caixa")  # 400 Bad Request


@app.route("/caixa/<id>", methods=["DELETE"])
def deleteCaixa(id):
    request.environ['user']

    caixaObj = caixa.query.filter_by(idCaixa=id).first()

    try:
        db.session.delete(caixaObj)
        db.session.commit()
        return geraResponse(200, "Caixa", caixaObj.toJson(), "Caixa deletado")
    except Exception as e:
        print(e)
        return geraResponse(400, "Caixa", {}, "Erro ao deletar Caixa")


@app.route("/marca", methods=["GET"])
def selecionaMarcas():
    # Requisita o middleware para acessar a rota
    request.environ['user']
    body = []

    try:
        m, c = aliased(marca), aliased(categoria)
        # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
        result = db.session.query(m.idmarca, m.nomemarca, c.idcategoria, c.nomecategoria). \
            select_from(m). \
            join(c, m.idcategoria == c.idcategoria).all()
        obj = {}
        cont = 0

        for i in result:
            for j in i:
                if cont == 0:
                    obj["idMarca"] = j
                if cont == 1:
                    obj["nomeMarca"] = j
                if cont == 2:
                    obj["idCategoria"] = j
                if cont == 3:
                    obj["nomeCategoria"] = j
                cont += 1
            body.append(obj)
            cont = 0
            obj = {}
        
        return geraResponse(200, "Marcas", body, "Ok")
    except Exception as e:
        pprint("Categoria: " + str(e))
        return geraResponse(400, "Marcas", body, "Erro ao selecionar categorias")


@app.route("/marca", methods=["POST"])
def InserirMarca():
    body = request.get_json()  # Requisita o body na requisição

    if body is None:  # Se o body estiver vazio ou não existir, então retorna response
        return geraResponse(400, "Marca", {}, "Sem o JSON")

    try:
        for i in ['nomeMarca', 'idCategoria']:
            if i not in body:
                return geraResponse(400, "Marca", {}, "without: " + i)

        nomeMarca = body['nomeMarca']
        idCategoria = body['idCategoria']
        marcaObj = marca(nomemarca=nomeMarca, idcategoria=idCategoria)

        db.session.add(marcaObj)  # Insere no banco de dados
        db.session.commit()  # Realiza Commit
        return geraResponse(201, "Marca", marcaObj.toJson(), "Marca inserida com sucesso")
    except Exception as e:
        print(e)
        return geraResponse(400, "Marca", {}, "Erro ao inserir Marca")  # 400 Bad Request


@app.route("/marca/<id>", methods=["DELETE"])
def deleteMarca(id):
    request.environ['user']

    try:
        marcaObj = marca.query.filter_by(idmarca=id).first()
        if marcaObj is None:
            return geraResponse(201, "Marca", {}, "Esta marca não existe")
        db.session.delete(marcaObj)
        db.session.commit()
        return geraResponse(200, "Marca", marcaObj.toJson(), "Marca deletada")
    except Exception as e:
        print(e)
        return geraResponse(400, "Marca", {}, "Erro ao deletar Marca")


@app.route("/produto", methods=["GET"])
def selecionaProdutos():
    # Requisita o middleware para acessar a rota
    request.environ['user']
    body = []

    try:
        prod, marc, categ = aliased(produto), aliased(marca), aliased(categoria)
        # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
        result = db.session.query(prod.idproduto, prod.nomeproduto, prod.preco, marc.idmarca, marc.nomemarca,
                                  categ.idcategoria, categ.nomecategoria). \
            select_from(prod). \
            join(marc, marc.idmarca == prod.idmarca). \
            join(categ, marc.idcategoria == categ.idcategoria).\
            all()
        print(result)
        obj = {}
        cont = 0

        for i in result:
            for j in i:
                print(j)
                if cont == 0:
                    obj["idProduto"] = j
                if cont == 1:
                    obj["nomeProduto"] = j
                if cont == 2:
                    obj["preco"] = j
                if cont == 3:
                    obj["idMarca"] = j
                if cont == 4:
                    obj["nomMarca"] = j
                if cont == 5:
                    obj["idCategoria"] = j
                if cont == 5:
                    obj["nomeCategoria"] = j
                cont += 1
            body.append(obj)
            cont = 0
            obj = {}

        return geraResponse(200, "Produto", body, "Ok")
    except Exception as e:
        pprint("Produto: " + str(e))
        return geraResponse(400, "Produto", body, "Erro ao selecionar Produto")


@app.route("/produto", methods=["POST"])
def InserirProduto():
    body = request.get_json()  # Requisita o body na requisição

    if body is None:  # Se o body estiver vazio ou não existir, então retorna response
        return geraResponse(400, "Produto", {}, "Sem o JSON")

    try:
        for i in ['nomeProduto', 'Preco', 'idMarca']:
            if i not in body:
                return geraResponse(400, "Produto", {}, "without: " + i)

        nomeProduto = body['nomeProduto']
        Preco = body['Preco']
        idMarca = body['idMarca']
        produtoObj = produto(nomeproduto=nomeProduto, preco=Preco, idmarca=idMarca)

        db.session.add(produtoObj)  # Insere no banco de dados
        db.session.commit()  # Realiza Commit
        return geraResponse(201, "Produto", produtoObj.toJson(), "Marca inserida com sucesso")
    except Exception as e:
        print(e)
        return geraResponse(400, "Produto", {}, "Erro ao inserir Marca")  # 400 Bad Request


@app.route("/produto/<id>", methods=["DELETE"])
def deleteProduto(id):
    request.environ['user']
    try:
        produtoObj = produto.query.filter_by(idproduto=id).first()
        if produtoObj is None:
            return geraResponse(201, "Produto", {}, "Este produto não existe")
        db.session.delete(produtoObj)
        db.session.commit()
        return geraResponse(200, "Produto", produtoObj.toJson(), "Produto deletado")
    except Exception as e:
        print(e)
        return geraResponse(400, "Produto", {}, "Erro ao deletar Produto")





def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
