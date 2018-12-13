from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'
db = SQLAlchemy(app, model_class=Base)


# =============================================================================
# Models
# =============================================================================
class Trabalha(Base):
    __tablename__ = 'trabalha'
    # Chaves
    funcionario_cpf = db.Column(db.String(20), db.ForeignKey('funcionario.cpf'),
                                primary_key=True)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorio.id'),
                               primary_key=True)
    # Relações
    funcionario = db.relationship('Funcionario',
                                  back_populates='consultorios')
    consultorio = db.relationship('Consultorio',
                                  back_populates='funcionarios')

    def __init__(self, funcionario, consultorio):
        self.funcionario_cpf = funcionario.cpf
        self.consultorio_id = consultorio.id
        self.funcionario = funcionario
        self.consultorio = consultorio

    def __repr__(self):
        return "Associação(Funcionario(Nome: {}) Trabalha em Consultorio(Nome: {})".format(
            self.funcionario.nome, self.consultorio.nome
        )


class Ficha(Base):
    __tablename__ = 'ficha'
    # Chaves
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    paciente_cpf = db.Column(db.String(20), db.ForeignKey('paciente.cpf'))
    medico_cpf = db.Column(db.String(20), db.ForeignKey('medico.cpf'))
    sala_numero = db.Column(db.String(40), db.ForeignKey('sala.numero'))

    # Relações
    paciente = db.relationship('Paciente', back_populates='consultas')
    medico = db.relationship('Medico', back_populates='consultas')
    sala = db.relationship('Sala', back_populates='consultas')

    def __init__(self, paciente, medico, sala):
        self.paciente = paciente
        self.medico = medico
        self.sala = sala

    def __repr__(self):
        return "Ficha(Paciente(Nome: {}), Medico(Nome: {}), Sala(Numero: {})".format(
            self.paciente.nome, self.medico.nome, self.sala.numero
        )


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
    plano_de_saude = db.Column(db.String(40),
                               db.ForeignKey('plano_de_saude.nome_da_empresa'),
                               nullable=False)
    consultas = db.relationship('Ficha', back_populates='paciente')

    def __init__(self, cpf, nome, telefone, email, endereco,
                 data_de_nascimento, historico, sexo, plano_de_saude):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.data_de_nascimento = data_de_nascimento
        self.historico = historico
        self.sexo = sexo
        self.plano_de_saude = plano_de_saude

    def __repr__(self):
        return "Paciente(Nome: {}, CPF: {}, telefone: {}, email: {}, endereco: {}, data_de_nascimento: {}, historico: {}, sexo: {}, plano_de_saude: {})".format(self.nome,
            self.cpf, self.telefone, self.email, self.endereco,
            self.data_de_nascimento, self.historico, self.sexo,
            self.plano_de_saude)


class PlanoDeSaude(Base):
    __tablename__ = 'plano_de_saude'
    nome_da_empresa = db.Column(db.String(40), primary_key=True,
                                nullable=False)
    cnpj = db.Column(db.String(30), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    site = db.Column(db.String(100), nullable=False)
    pacientes = db.relationship('Paciente',
                                lazy=True)

    def __init__(self, nome_da_empresa, cnpj, telefone, email, site):
        self.nome_da_empresa = nome_da_empresa
        self.cnpj = cnpj
        self.telefone = telefone
        self.email = email
        self.site = site

    def __repr__(self):
        return "PlanoDeSaude(Nome da Empresa: {}, CNPJ: {},\nPacientes: {})".format(
            self.nome_da_empresa, self.cnpj, self.pacientes
        )


class Sala(Base):
    __tablename__ = 'sala'
    numero = db.Column(db.String(40), primary_key=True, nullable=False)
    equipamentos = db.Column(db.String(100), nullable=False)
    consultas = db.relationship('Ficha', back_populates='sala')

    def __init__(self, numero, equipamentos):
        self.numero = numero
        self.equipamentos = equipamentos

    def __repr__(self):
        return "Sala(Numero: {}, Equipamentos: {})".format(
            self.numero, self.equipamentos
        )


class Funcionario(Base):
    __tablename__ = 'funcionario'
    cpf = db.Column(db.String(20), primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    periodo_de_trabalho = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    consultorios = db.relationship('Trabalha', back_populates='funcionario')
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': type
    }

    def __init__(self, cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.periodo_de_trabalho = periodo_de_trabalho
        self.salario = salario

    def __repr__(self):
        return "{}(Nome: {}, CPF: {}, telefone: {}, endereco: {}, email: {}, periodo_de_trabalho: {}, salario: {}".format(
            self.type, self.nome, self.cpf, self.telefone, self.endereco,
            self.email, self.periodo_de_trabalho, self.salario
        )


class Medico(Funcionario):
    __tablename__ = 'medico'
    cpf = db.Column(db.String(20), db.ForeignKey('funcionario.cpf'),
                    primary_key=True)
    crm = db.Column(db.String(20), nullable=False)
    especialidades = db.Column(db.String(120), nullable=False)
    consultas = db.relationship('Ficha', back_populates='medico')

    __mapper_args__ = {
        'polymorphic_identity': 'medico',
    }

    def __init__(self, cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario, crm, especialidades):
        Funcionario.__init__(self, cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario)
        self.crm = crm
        self.especialidades = especialidades

    def __repr__(self):
        return "Medico(Nome: {}, CRM: {}, CPF: {},\nConsultorios: {}".format(
            self.nome, self.crm, self.cpf, self.consultorios)


class Outros(Funcionario):
    __tablename__ = 'outros'
    cpf = db.Column(db.String(20), db.ForeignKey('funcionario.cpf'),
                    primary_key=True)
    funcao = db.Column(db.String(30), nullable=False)
    formacao = db.Column(db.String(120), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'outros',
    }

    def __init__(self, cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario, funcao, formacao):
        Funcionario.__init__(self, cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario)
        self.funcao = funcao
        self.formacao = formacao

    def __repr__(self):
        return "Outros(Nome: {}, Função: {}, CPF: {}".format(
            self.nome, self.funcao, self.cpf)


class Consultorio(Base):
    __tablename__ = 'consultorio'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    funcionarios = db.relationship('Trabalha', back_populates='consultorio')

    def __init__(self, telefone, endereco, nome):
        self.telefone = telefone
        self.endereco = endereco
        self.nome = nome

    def __repr__(self):
        return "Consultorio(ID: {}, Nome: {}, Telefone: {})".format(
            self.id, self.nome, self.telefone
        )


# =============================================================================
# Controllers
# =============================================================================

def criar_paciente(cpf, nome, telefone, email, endereco,
                   data_de_nascimento, historico, sexo, plano_de_saude):
    paciente = Paciente(cpf, nome, telefone, email, endereco,
                        data_de_nascimento, historico, sexo, plano_de_saude)
    db.session.add(paciente)
    db.session.commit()
    return paciente


def criar_plano_de_saude(nome_da_empresa, cnpj, telefone, email, site):
    plano_de_saude = PlanoDeSaude(nome_da_empresa, cnpj, telefone, email, site)
    db.session.add(plano_de_saude)
    db.session.commit()
    return plano_de_saude


def criar_sala(numero, equipamentos):
    sala = Sala(numero, equipamentos)
    db.session.add(sala)
    db.session.commit()
    return sala


def criar_medico(cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario, crm, especialidades):
    medico = Medico(cpf, nome, telefone, endereco, email,
                    periodo_de_trabalho, salario, crm, especialidades)
    db.session.add(medico)
    db.session.commit()
    return medico


def criar_outros(cpf, nome, telefone, endereco, email,
                 periodo_de_trabalho, salario, funcao, formacao):
    outro = Outros(cpf, nome, telefone, endereco, email,
                   periodo_de_trabalho, salario, funcao, formacao)
    db.session.add(outro)
    db.session.commit()
    return outro


def criar_consultorio(telefone, endereco, nome):
    consultorio = Consultorio(telefone, endereco, nome)
    db.session.add(consultorio)
    db.session.commit()
    return consultorio


def associar_trabalha(funcionario, consultorio):
    trabalha = Trabalha(funcionario, consultorio)
    db.session.add(trabalha)
    db.session.commit()
    return trabalha


def associar_ficha(paciente, medico, sala):
    ficha = Ficha(paciente, medico, sala)
    db.session.add(ficha)
    db.session.commit()
    return ficha


# =============================================================================
# Views
# =============================================================================

@app.route("/teste")
def teste():
    try:
        db.create_all()
        for table in db.metadata.sorted_tables:
            db.session.execute(table.delete())
        db.session.commit()
        criar_plano_de_saude("Porto", "1234567845561", "121516515",
                             "dae@cnsd.com", "www.porto.com")
        paciente = criar_paciente("123", "Felipe", "987654321", "joao@gmail.com",
                       "Rua Três", "23/12/1987", "Nada", "Masculino", "Porto")
        sala = criar_sala("32", "maquinas diversas")
        medico = criar_medico("525252", "Dr. Fernando", "123456", "Av. dos Medicos",
                     "fern@ndo.com", "Diurno", "12000", "789789", "Nenhuma")
        criar_outros("121212", "Pedro Dante", "12121354685",
                     "Av. dos Segurancas", "pedro@email.com", "noturno",
                     "3000", "Seguranca", "Engenharia de Producao")
        consultorio = criar_consultorio("15651651", "Alameda Consultorial", "Primordial")
        consultorio2 = criar_consultorio("785418", "Alameda Nao Consultorial", "O outro")
        associar_trabalha(medico, consultorio)
        associar_trabalha(medico, consultorio2)
        associar_ficha(paciente, medico, sala)

        return str(Ficha.query.all())
    except Exception as e:
        return str(e)

@app.route("/pacientes")
def pacientes():
    return "Pagina de pacientes"



if __name__ == "__main__":
    app.run()
