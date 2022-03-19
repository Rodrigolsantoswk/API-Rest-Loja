from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class caixa(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idcaixa = db.Column(db.Integer, primary_key=True)
    nomecaixa = db.Column(db.String(30), nullable=False)
    datanascimentocaixa = db.Column(db.Date, nullable=False)
    inseridoem = db.Column(db.DateTime)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idCaixa": self.idcaixa,
            "nomeCaixa": self.nomecaixa,
            "dataNascimentoCaixa": str(self.datanascimentocaixa),
            "inseridoEm": str(self.inseridoem)
        }
