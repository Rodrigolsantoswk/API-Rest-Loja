from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class venda(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idvenda = db.Column(db.Integer, primary_key=True)
    dtiniciovenda = db.Column(db.DateTime, nullable=False)
    dtfimvenda = db.Column(db.DateTime, nullable=True)
    idcaixa = db.Column(db.Integer, db.ForeignKey('caixa.idcaixa'), nullable=False)
    vendaProduto = db.Column(db.ForeignKey('venda_produto.idvenda'), nullable=False)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idVenda": self.idvenda,
            "dtInicioVenda": str(self.dtiniciovenda),
            "dtFimVenda": str(self.dtfimvenda),
            "idCaixa": self.idcaixa
        }
