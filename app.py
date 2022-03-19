from flask import request, Response
import json
from sqlalchemy.orm import aliased
from pprint import pprint
from dbconfig import db, app
from datetime import datetime
from caixa import caixa
from marca import marca
from categoria import categoria
from produto import produto
from venda import venda
from venda_produto import venda_produto


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
            join(categ, marc.idcategoria == categ.idcategoria). \
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
                if cont == 6:
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


@app.route("/venda", methods=["GET"])
def selecionaVenda():
    # Requisita o middleware para acessar a rota
    request.environ['user']
    body = []

    try:
        cx, vnd = aliased(caixa), aliased(venda)
        # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
        result = db.session.query(vnd.idvenda, vnd.dtiniciovenda, vnd.dtfimvenda, cx.idcaixa, cx.nomecaixa,
                                  cx.datanascimentocaixa, cx.inseridoem). \
            select_from(vnd). \
            join(cx, cx.idcaixa == vnd.idcaixa). \
            all()
        print(result)
        obj = {}
        cont = 0

        for i in result:
            for j in i:
                if cont == 0:
                    obj["idVenda"] = j
                if cont == 1:
                    obj["dtInicioVenda"] = str(j)
                if cont == 2:
                    obj["dtFimVenda"] = str(j)
                if cont == 3:
                    obj["idCaixa"] = j
                if cont == 4:
                    obj["nomeCaixa"] = j
                if cont == 5:
                    obj["dataNascimentoCaixa"] = str(j)
                if cont == 6:
                    obj["inseridoEm"] = str(j)
                cont += 1
            body.append(obj)
            cont = 0
            obj = {}

        return geraResponse(200, "Produto", body, "Ok")
    except Exception as e:
        pprint("Produto: " + str(e))
        return geraResponse(400, "Produto", body, "Erro ao selecionar Produto")


@app.route("/FinalizarVenda/<id>", methods=["PUT"])
def atualizarVenda(id):
    request.environ['user']

    vendaObj = venda.query.filter_by(idvenda=id).first()

    body = request.get_json()

    try:
        if 'dtInicioVenda' in body:
            vendaObj.dtiniciovenda = body['dtiniciovenda']
        if 'dtFimVenda' in body:
            now = datetime.now()
            vendaObj.dtfimvenda = now
        if 'idCaixa' in body:
            vendaObj.idcaixa = body['idcaixa']

        if len(body) < 1:
            return geraResponse(400, "Venda", {}, "JSON não pode estar vazio")
        else:
            lista = ['dtInicioVenda', 'dtFimVenda', 'idCaixa']
            lista2 = body.keys()
            cont = 0
            soma = 0
            lista3 = []
            for i in lista2:
                for j in lista:
                    if i == j:
                        cont += 1
                if cont == 0:
                    soma += 1
                    lista3.append(i)

                cont = 0

            if soma > 0:
                return geraResponse(400, "Venda", {}, "Parâmetro(s) enviado(s) não permitido(s)" + str(lista3))

        db.session.add(vendaObj)
        db.session.commit()
        return geraResponse(200, "Venda", vendaObj.toJson(), "Dado(s) alterado(s) com sucesso")
    except Exception as e:
        print(e)
        return geraResponse(400, "Venda", {}, "Erro ao atualizar")


@app.route("/venda_produto/<id>", methods=["GET"])
def selecionaVenda_produto(id):
    # Requisita o middleware para acessar a rota
    request.environ['user']
    body = []
    print(id)
    try:
        # Pesquisa o objeto no banco de dados e retorna uma lista de objetos
        result = db.session.query(venda_produto.idvenda_produto, venda_produto.preco, venda.idvenda, venda.dtiniciovenda
                                  , venda.dtfimvenda, caixa.idcaixa, caixa.nomecaixa, caixa.datanascimentocaixa,
                                  caixa.inseridoem, produto.idproduto, produto.nomeproduto, produto.preco
                                  , marca.idmarca, marca.nomemarca, categoria.idcategoria, categoria.nomecategoria). \
            select_from(venda_produto). \
            join(venda, venda.idvenda == venda_produto.idvenda). \
            join(produto, produto.idproduto == venda_produto.idproduto). \
            join(caixa, caixa.idcaixa == venda.idcaixa). \
            join(marca, marca.idmarca == produto.idmarca). \
            join(categoria, categoria.idcategoria == marca.idmarca). \
            filter(venda.idvenda == id).all()
        print(result)
        obj = {}
        cont = 0

        for i in result:
            for j in i:
                if cont == 0:
                    obj["idVenda_Produto"] = j
                if cont == 1:
                    obj["Preco"] = j
                if cont == 2:
                    obj["idVenda"] = j
                if cont == 3:
                    obj["dtInicioVenda"] = str(j)
                if cont == 4:
                    obj["dtFimVenda"] = str(j)
                if cont == 5:
                    obj["idCaixa"] = j
                if cont == 6:
                    obj["nomeCaixa"] = j
                if cont == 7:
                    obj["dataNascimentoCaixa"] = str(j)
                if cont == 8:
                    obj["inseridoEm"] = str(j)
                if cont == 9:
                    obj["idProduto"] = j
                if cont == 10:
                    obj["nomeProduto"] = j
                if cont == 11:
                    obj["Preco"] = j
                if cont == 12:
                    obj["idMarca"] = j
                if cont == 13:
                    obj["nomeMarca"] = j
                if cont == 14:
                    obj["idCategoria"] = j
                if cont == 15:
                    obj["nomeCategoria"] = j
                cont += 1
            body.append(obj)
            cont = 0
            obj = {}

        return geraResponse(200, "venda_produto", body, "OK")
    except Exception as e:
        return geraResponse(400, "venda_produto", {}, "Erro ao selecionar venda_produto")


@app.route("/venda_produto/<id>", methods=["DELETE"])
def deleteVendaProduto(id):
    request.environ['user']
    try:
        vendaProdutoObj = venda_produto.query.filter_by(idvenda_produto=id).first()
        if vendaProdutoObj is None:
            return geraResponse(201, "venda_produto", {}, "Este venda_produto não existe")
        db.session.delete(vendaProdutoObj)
        db.session.commit()
        return geraResponse(200, "venda_produto", vendaProdutoObj.toJson(), "venda_produto deletado")
    except Exception as e:
        print(e)
        return geraResponse(400, "venda_produto", {}, "Erro ao deletar venda_produto")


@app.route("/venda_produto", methods=["POST"])
def InserirVenda_Produto():
    body = request.get_json()  # Requisita o body na requisição

    if body is None:  # Se o body estiver vazio ou não existir, então retorna response
        return geraResponse(400, "venda_produto", {}, "Sem o JSON")

    try:
        for i in ['idVenda', 'idProduto']:
            if i not in body:
                return geraResponse(400, "Produto", {}, "without: " + i)

        produtoObj = produto.query.filter_by(idproduto=body['idProduto']).first()

        idVenda = body['idVenda']
        idProduto = body['idProduto']
        Preco = produtoObj.preco

        venda_produtoObj = venda_produto(idvenda=idVenda, preco=Preco, idproduto=idProduto)

        db.session.add(venda_produtoObj)  # Insere no banco de dados
        db.session.commit()  # Realiza Commit
        return geraResponse(201, "venda_produto", produtoObj.toJson(), "venda_produto inserida com sucesso")
    except Exception as e:
        print(e)
        return geraResponse(400, "venda_produto", {}, "Erro ao inserir venda_produto")  # 400 Bad Request


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
