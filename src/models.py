from src import db, Base

len_cpf = 11
len_cnpj = 14


class Trabalha(Base):
    __tablename__ = 'trabalha'
    # Chave
    funcionario_cpf = db.Column(db.String(len_cpf),
                                db.ForeignKey('funcionario.cpf'),
                                primary_key=True)
    consultorio_id  = db.Column(db.Integer,
                                db.ForeignKey('consultorio.id'),
                                primary_key=True)
    # Relações
    funcionario = db.relationship('Funcionario',
                                  back_populates='consultorios')
    consultorio = db.relationship('Consultorio',
                                  back_populates='funcionarios')

    def __init__(self, funcionario_cpf, consultorio_id):
        self.funcionario_cpf = funcionario_cpf
        self.consultorio_id = consultorio_id

    def __repr__(self):
        return ("[Trabalha]:\n" +
                "\tFuncionario(Nome: {})\n".format(self.funcionario.nome) +
                "\tConsultorio(Nome: {})\n".format(self.consultorio.nome)
                )


class Ficha(Base):
    __tablename__ = 'ficha'
    # Chave
    id = db.Column(db.Integer, primary_key=True)
    paciente_cpf = db.Column(db.String(len_cpf), db.ForeignKey('paciente.cpf'))
    medico_cpf   = db.Column(db.String(len_cpf), db.ForeignKey('medico.cpf'))
    sala_id      = db.Column(db.Integer, db.ForeignKey('sala.id'))

    # Atributos
    comentarios = db.Column(db.String(500))
    sintomas    = db.Column(db.String(500))
    exames      = db.Column(db.String(500))

    # Relações
    paciente = db.relationship('Paciente', back_populates='fichas')
    medico   = db.relationship('Medico', back_populates='fichas')
    sala     = db.relationship('Sala', back_populates='fichas')

    def __init__(self, paciente_cpf, medico_cpf, sala_id):
        self.paciente_cpf = paciente_cpf
        self.medico_cpf = medico_cpf
        self.sala_id = sala_id

    def __repr__(self):
        return ("[Ficha] ID: " + self.id +
                "\n\t-paciente_cpf: " + self.paciente_cpf +
                "\n\t-medico_cpf: " + self.medico_cpf +
                "\n\t-sala_id: " + self.sala_id +
                "\n\t-comentarios: " + self.comentarios +
                "\n\t-sintomas: " + self.sintomas +
                "\n\t-exames: " + self.exames
                )


class Contem(Base):
    __tablename__ = 'contem'
    # Chave
    sala_id        = db.Column(db.Integer, db.ForeignKey('sala.id'),
                               primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamento.id'),
                               primary_key=True)
    sala = db.relationship('Sala', back_populates='equipamentos')
    equipamento = db.relationship('Equipamento', back_populates='salas')

    def __init__(self, sala, equipamento):
        self.paciente_cpf

    def __repr__(self):
        return str(self.__dict__)


class Paciente(Base):
    __tablename__ = 'paciente'

    # Chave
    cpf            = db.Column(db.String(len_cpf), primary_key=True)

    # Atributos
    nome                = db.Column(db.String(100), nullable=False)
    email               = db.Column(db.String(100), nullable=False)
    telefone            = db.Column(db.String(100), nullable=False)
    endereco            = db.Column(db.String(100), nullable=False)
    data_de_nascimento  = db.Column(db.String(100), nullable=False)
    sexo                = db.Column(db.String(100), nullable=False)
    historico           = db.Column(db.String(100))

    # Relações
    fichas              = db.relationship('Ficha', back_populates='paciente')
    plano_de_saude_cnpj = db.Column(db.String(len_cnpj),
        db.ForeignKey('plano_de_saude.cnpj')
    )

    def __init__(self, cpf, nome, email, telefone, endereco,
                 data_de_nascimento, sexo, historico, plano_de_saude_cnpj):
        self.cpf                 = cpf
        self.nome                = nome
        self.email               = email
        self.telefone            = telefone
        self.endereco            = endereco
        self.data_de_nascimento  = data_de_nascimento
        self.sexo                = sexo
        self.historico           = historico
        self.plano_de_saude_cnpj = plano_de_saude_cnpj

    def __repr__(self):
        return ("[Paciente] CPF: " + self.cpf +
                "\n\t-nome: " + self.nome +
                "\n\t-email: " + self.email +
                "\n\t-telefone: " + self.telefone +
                "\n\t-endereco: " + self.endereco +
                "\n\t-data_de_nascimento: " + self.data_de_nascimento +
                "\n\t-sexo: " + self.sexo +
                "\n\t-historico: " + self.historico +
                "\n\t-plano_de_saude:" + self.plano_de_saude_cnpj +
                "\n\t-fichas:" + str(self.fichas) +
                "\n" + "_" * 20
                )


class PlanoDeSaude(Base):
    __tablename__ = 'plano_de_saude'

    # Chave
    cnpj = db.Column(db.String(len_cnpj), primary_key=True)

    # Atributos
    nome_da_empresa = db.Column(db.String(40), nullable=False)
    telefone        = db.Column(db.String(100), nullable=False)
    email           = db.Column(db.String(100), nullable=False)
    site            = db.Column(db.String(100), nullable=False)

    # Relações
    clientes = db.relationship('Paciente', lazy=True)

    def __init__(self, cnpj, nome_da_empresa, telefone, email, site):
        self.cnpj            = cnpj
        self.nome_da_empresa = nome_da_empresa
        self.telefone        = telefone
        self.email           = email
        self.site            = site

    def __repr__(self):
        return ("[Plano de Saúde] CNPJ: " + self.cnpj +
                "\n\t-nome_da_empresa: " + self.nome_da_empresa +
                "\n\t-telefone: " + self.telefone +
                "\n\t-email: " + self.email +
                "\n\t-site: " + self.site +
                "\n" + "_" * 20
                )


class Sala(Base):
    __tablename__ = 'sala'

    # Chave
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    # Atributos
    numero = db.Column(db.String(40), nullable=False)
    setor  = db.Column(db.String(40), nullable=False)
    ramal  = db.Column(db.String(40), nullable=False)

    # Relações
    fichas         = db.relationship('Ficha', back_populates='sala')
    equipamentos   = db.relationship('Contem', back_populates='sala')
    consultorio    = db.relationship('Consultorio', back_populates='salas')
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorio.id'))

    def __init__(self, numero, setor, ramal, consultorio_id):
        self.numero         = numero
        self.setor          = setor
        self.ramal          = ramal
        self.consultorio_id = consultorio_id

    def __repr__(self):
        return ("[Sala] ID: " + self.id +
                "\n\t-numero: " + self.numero +
                "\n\t-setor: " + self.setor +
                "\n\t-ramal: " + self.ramal
                )


class Funcionario(Base):
    __tablename__ = 'funcionario'

    # Chave
    cpf = db.Column(db.String(len_cpf), primary_key=True, nullable=False)

    # Atributos
    nome                = db.Column(db.String(100), nullable=False)
    email               = db.Column(db.String(100), nullable=False)
    telefone            = db.Column(db.String(100), nullable=False)
    endereco            = db.Column(db.String(100), nullable=False)
    formacao            = db.Column(db.String(100), nullable=True)
    salario             = db.Column(db.String(100), nullable=False)
    periodo_de_trabalho = db.Column(db.String(100), nullable=False)

    # Relações
    consultorios = db.relationship('Trabalha', back_populates='funcionario')

    # Especificação
    type = db.Column(db.String(20), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': type
    }

    def __init__(self, cpf, nome, email, telefone, endereco, formacao,
                 salario, periodo_de_trabalho):
        self.cpf                 = cpf
        self.nome                = nome
        self.email               = email
        self.telefone            = telefone
        self.endereco            = endereco
        self.formacao            = formacao
        self.salario             = salario
        self.periodo_de_trabalho = periodo_de_trabalho

    def __repr__(self):
        return ("[Funcionario] CPF: " + self.cpf +
                "\n\t-nome: " + self.nome +
                "\n\t-telefone: " + self.telefone +
                "\n\t-endereco: " + self.endereco +
                "\n\t-email: " + self.email +
                "\n\t-periodo_de_trabalho: " + self.periodo_de_trabalho +
                "\n\t-salario: " + self.salario +
                "\n\t-formacao: " + self.formacao)


class Medico(Funcionario):
    __tablename__ = 'medico'

    # Chave
    cpf = db.Column(db.String(len_cpf), db.ForeignKey('funcionario.cpf'),
                    primary_key=True)

    # Atributos
    crm             = db.Column(db.String(20), nullable=False)
    especialidades  = db.Column(db.String(120), nullable=False)

    # Relações
    fichas          = db.relationship('Ficha', back_populates='medico')

    # Especificação
    __mapper_args__ = {
        'polymorphic_identity': 'medico',
    }

    def __init__(self, cpf, nome, email, telefone, endereco, formacao,
                 salario, periodo_de_trabalho, crm, especialidades):
        super().__init__(cpf, nome, email, telefone, endereco, formacao,
                         salario, periodo_de_trabalho)
        self.crm = crm
        self.especialidades = especialidades

    def __repr__(self):
        return ("[Médico] CPF: " + self.cpf +
                "\n\t-nome: " + self.nome +
                "\n\t-email: " + self.email +
                "\n\t-telefone: " + self.telefone +
                "\n\t-endereco: " + self.endereco +
                "\n\t-formacao: " + self.formacao +
                "\n\t-salario: " + self.salario +
                "\n\t-periodo_de_trabalho: " + self.periodo_de_trabalho +
                "\n\t-crm: " + self.crm +
                "\n\t-especialidades: " + self.especialidades
                )


class Assistente(Funcionario):
    __tablename__ = 'assistente'

    # Chave
    cpf = db.Column(db.String(len_cpf), db.ForeignKey('funcionario.cpf'),
                    primary_key=True)

    # Atributos
    funcao = db.Column(db.String(30), nullable=False)

    # Especificação
    __mapper_args__ = {
        'polymorphic_identity': 'assistente',
    }

    def __init__(self, cpf, nome, email, telefone, endereco, formacao,
                 salario, periodo_de_trabalho, funcao):
        super().__init__(cpf, nome, email, telefone, endereco, formacao,
                       salario, periodo_de_trabalho)
        self.funcao = funcao

    def __repr__(self):
        return ("[Assistente] CPF: " + self.cpf +
                "\n\t-nome: " + self.nome +
                "\n\t-email: " + self.email +
                "\n\t-telefone: " + self.telefone +
                "\n\t-endereco: " + self.endereco +
                "\n\t-formacao: " + self.formacao +
                "\n\t-salario: " + self.salario +
                "\n\t-periodo_de_trabalho: " + self.periodo_de_trabalho +
                "\n\t-funcao: " + self.funcao)


class Consultorio(Base):
    __tablename__ = 'consultorio'
    # Chave
    id = db.Column(db.Integer, primary_key=True)

    # Atributos
    endereco = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)

    # Relações
    funcionarios = db.relationship('Trabalha', back_populates='consultorio')
    salas        = db.relationship('Sala', back_populates='consultorio')

    def __init__(self, telefone, endereco, nome):
        self.telefone = telefone
        self.endereco = endereco
        self.nome = nome

    def __repr__(self):
        return str([(a + '\n') for a in self.__dict__])


class Equipamento(Base):
    __tablename__ = 'equipamento'

    # Chave
    id = db.Column(db.Integer, primary_key=True)

    # Atributos
    nome       = db.Column(db.String(50))
    fabricante = db.Column(db.String(50))
    descricao  = db.Column(db.String(500))

    # Relações
    salas = db.relationship('Contem', back_populates='equipamento')
