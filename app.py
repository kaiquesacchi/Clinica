from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config['TESTING'] = True
Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'
db = SQLAlchemy(app, model_class=Base)


class Paciente(Base):
    __tablename__ = 'paciente'
    cpf = db.Column(db.String(20), primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    data_de_nascimento = db.Column(db.String(100), nullable=False)
    historico = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(100), nullable=False)

    def __init__(self, cpf, nome, telefone, email, endereco,
                 data_de_nascimento, historico, sexo):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.data_de_nascimento = data_de_nascimento
        self.historico = historico
        self.sexo = sexo

    def __repr__(self):
        return "Paciente(Nome: {}, CPF: {}, telefone: {}, email: {}, endereco: {}, data_de_nascimento: {}, historico: {}, sexo: {})".format(self.nome,
            self.cpf, self.telefone, self.email, self.endereco,
            self.data_de_nascimento, self.historico, self.sexo)


@app.route("/teste")
def teste():
    try:
        db.create_all()
        paciente = Paciente(cpf="123", nome="João",
                            telefone="987654321",
                            email="joao@gmail.com", endereco="Rua Três",
                            data_de_nascimento="23/12/1987",
                            historico="Nada", sexo="Masculino")
        db.session.add(paciente)
        db.session.commit()
        return str(Paciente.query.all())
    except Exception as e:
        return str(e)



if __name__ == "__main__":
    app.run()