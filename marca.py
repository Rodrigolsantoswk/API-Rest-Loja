from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class marca(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idmarca = db.Column(db.Integer, primary_key=True)
    nomemarca = db.Column(db.String(30), nullable=False)
    idcategoria = db.Column(db.Integer, db.ForeignKey('categoria.idcategoria'), nullable=False)
    produto = db.Column(db.Integer, db.ForeignKey('produto.idmarca'), nullable=False)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idMarca": self.idmarca,
            "nomeMarca": self.nomemarca,

        }
