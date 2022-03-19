from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class venda_produto(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idvenda_produto = db.Column(db.Integer, primary_key=True)
    preco = db.Column(db.Float, nullable=False)
    idproduto = db.Column(db.Integer, db.ForeignKey('produto.idproduto'), nullable=True)
    idvenda = db.Column(db.Integer, db.ForeignKey('venda.idvenda'), nullable=False)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idvenda_produto": self.idvenda_produto,
            "preco": self.preco,
            "idproduto": self.idproduto,
            "idvenda": self.idvenda
        }