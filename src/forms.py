from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class FiltroPaciente(FlaskForm):
    cpf = StringField('cpf')
    nome = StringField('nome')
    telefone = StringField('telefone')
    email = StringField('email')
    endereco = StringField('endereco')
    data_de_nascimento = StringField('data_de_nascimento')
    sexo = StringField('sexo')
    plano_de_saude = StringField('plano_de_saude')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class FiltroPlanoDeSaude(FlaskForm):
    nome_da_empresa = StringField('nome_da_empresa')
    cnpj = StringField('cnpj')
    telefone = StringField('telefone')
    email = StringField('email')
    site = StringField('site')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class FiltroSala(FlaskForm):
    numero = StringField('numero')
    equipamentos = StringField('equipamentos')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class FiltroMedico(FlaskForm):
    cpf = StringField('cpf')
    nome = StringField('nome')
    telefone = StringField('telefone')
    endereco = StringField('endereco')
    email = StringField('email')
    periodo_de_trabalho = StringField('periodo_de_trabalho')
    salario = StringField('salario')
    crm = StringField('crm')
    especialidades = StringField('especialidades')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class FiltroOutro(FlaskForm):
    cpf = StringField('cpf')
    nome = StringField('nome')
    telefone = StringField('telefone')
    endereco = StringField('endereco')
    email = StringField('email')
    periodo_de_trabalho = StringField('periodo_de_trabalho')
    salario = StringField('salario')
    funcao = StringField('funcao')
    formacao = StringField('formacao')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class FiltroConsultorio(FlaskForm):
    telefone = StringField('telefone')
    endereco = StringField('endereco')
    nome = StringField('nome')

    # Botões
    filtrar = SubmitField(label="Filtrar")
    criar = SubmitField(label="Criar")
    cancelar = SubmitField(label="Cancelar")


class Home(FlaskForm):
    paciente = SubmitField(label="Paciente")
    plano_de_saude = SubmitField(label="Plano de Saúde")
    sala = SubmitField(label="Sala")
    medico = SubmitField(label="Médico")
    outro = SubmitField(label="Outros Funcionários")
    consultorio = SubmitField(label="Consultório")
