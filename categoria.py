from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class categoria(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idCategoria = db.Column(db.Integer, primary_key=True)
    nomeCategoria = db.Column(db.String(30), nullable=False)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idCategoria": self.idCategoria,
            "nomeCateogoria": self.nomeCategoria
        }
