from dbconfig import db  # Importa o modelo gerado no arquivo dbconfig


# Nova classe modelo
class categoria(db.Model):
    # Criação dos atributos de classe igualmente ao banco de dados.
    idcategoria = db.Column(db.Integer, primary_key=True)
    nomecategoria = db.Column(db.String(30), nullable=False)
    marca = db.Column(db.Integer, db.ForeignKey('marca.idcategoria'), nullable=False)

    # Retorna um Json com os atributos da classe
    def toJson(self):
        return {
            "idCategoria": self.idcategoria,
            "nomeCateogoria": self.nomecategoria
        }
