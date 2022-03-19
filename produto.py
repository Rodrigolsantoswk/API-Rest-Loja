from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class produto(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idproduto = db.Column(db.Integer, primary_key=True)
    nomeproduto = db.Column(db.String(35), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    idmarca = db.Column(db.Integer, db.ForeignKey('marca.idmarca'), nullable=False)
    # produtoVenda = db.Column(db.Integer, db.ForeignKey('venda_produto.idproduto'), nullable=True)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idMarca": self.nomeproduto,
            "nomeMarca": self.preco,
            "idMarca": self.idmarca
        }
