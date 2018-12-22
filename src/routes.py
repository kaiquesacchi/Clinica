from flask import render_template, redirect, url_for
from src import app
from src.forms import *
from src.models import *


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


@app.route("/home", methods=('GET', 'POST'))
def home():
    form = Home(csrf_enabled=False)
    if form.validate_on_submit():
        if form.paciente.data: return redirect(url_for('paciente'))
        if form.plano_de_saude.data: return redirect(url_for('plano_de_saude'))
        if form.sala.data: return redirect(url_for('sala'))
        if form.medico.data: return redirect(url_for('medico'))
        if form.outro.data: return redirect(url_for('outro'))
        if form.consultorio.data: return redirect(url_for('consultorio'))
    return render_template("home.html", form=form)


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


@app.route("/filtrar-paciente", methods=('GET', 'POST'))
def paciente():
    form = FiltroPaciente(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_paciente(form.cpf.data, form.nome.data, form.telefone.data,
                           form.email.data, form.endereco.data,
                           form.data_de_nascimento.data, None,
                           form.sexo.data, form.plano_de_saude.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = Paciente.query.filter(
                (form.cpf.data == '' or Paciente.cpf == form.cpf.data),
                (form.nome.data == '' or Paciente.nome == form.nome.data),
                (form.telefone.data == '' or Paciente.telefone == form.telefone.data),
                (form.email.data == '' or Paciente.email == form.email.data),
                (form.endereco.data == '' or Paciente.endereco == form.endereco.data),
                (form.data_de_nascimento.data == '' or Paciente.data_de_nascimento == form.data_de_nascimento.data),
                (form.sexo.data == '' or Paciente.sexo == form.sexo.data),
                (form.plano_de_saude.data == '' or Paciente.plano_de_saude == form.plano_de_saude.data)
            ).all()
            return render_template("listar_paciente.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_pacientes.html", form=form)


@app.route("/filtrar-plano_de_saude", methods=('GET', 'POST'))
def plano_de_saude():
    form = FiltroPlanoDeSaude(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_plano_de_saude(form.nome_da_empresa.data, form.cnpj.data,
                                 form.telefone.data, form.email.data,
                                 form.site.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = PlanoDeSaude.query.filter(
                (form.nome_da_empresa.data == '' or PlanoDeSaude.nome_da_empresa == form.nome_da_empresa.data),
                (form.cnpj.data == '' or PlanoDeSaude.cnpj == form.cnpj.data),
                (form.telefone.data == '' or PlanoDeSaude.telefone == form.telefone.data),
                (form.email.data == '' or PlanoDeSaude.email == form.email.data),
                (form.site.data == '' or PlanoDeSaude.site == form.site.data)
            ).all()
            return render_template("listar_plano_de_saude.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_plano_de_saude.html", form=form)


@app.route("/filtrar-sala", methods=('GET', 'POST'))
def sala():
    form = FiltroSala(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_sala(form.numero.data, form.equipamentos.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = Sala.query.filter(
                (form.numero.data == '' or Sala.numero == form.numero.data),
                (form.equipamentos.data == '' or Sala.equipamentos == form.equipamentos.data)
            ).all()
            return render_template("listar_sala.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_sala.html", form=form)


@app.route("/filtrar-medico", methods=('GET', 'POST'))
def medico():
    form = FiltroMedico(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_medico(form.cpf.data, form.nome.data, form.telefone.data,
                         form.endereco.data, form.email.data,
                         form.periodo_de_trabalho.data, form.salario.data,
                         form.crm.data, form.especialidades.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = Medico.query.filter(
                (form.cpf.data == '' or Medico.cpf == form.cpf.data),
                (form.nome.data == '' or Medico.nome == form.nome.data),
                (form.telefone.data == '' or Medico.telefone == form.telefone.data),
                (form.endereco.data == '' or Medico.endereco == form.endereco.data),
                (form.email.data == '' or Medico.email == form.email.data),
                (form.periodo_de_trabalho.data == '' or Medico.periodo_de_trabalho == form.periodo_de_trabalho.data),
                (form.salario.data == '' or Medico.salario == form.salario.data),
                (form.crm.data == '' or Medico.crm == form.crm.data),
                (form.especialidades.data == '' or Medico.especialidades == form.especialidades.data)
            ).all()
            return render_template("listar_medico.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_medico.html", form=form)


@app.route("/filtrar-outro", methods=('GET', 'POST'))
def outro():
    form = FiltroOutro(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_outros(form.cpf.data, form.nome.data, form.telefone.data,
                         form.endereco.data, form.email.data,
                         form.periodo_de_trabalho.data, form.salario.data,
                         form.funcao.data, form.formacao.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = Outros.query.filter(
                (form.cpf.data == '' or Outros.cpf == form.cpf.data),
                (form.nome.data == '' or Outros.nome == form.nome.data),
                (form.telefone.data == '' or Outros.telefone == form.telefone.data),
                (form.endereco.data == '' or Outros.endereco == form.endereco.data),
                (form.email.data == '' or Outros.email == form.email.data),
                (form.periodo_de_trabalho.data == '' or Outros.periodo_de_trabalho == form.periodo_de_trabalho.data),
                (form.salario.data == '' or Outros.salario == form.salario.data),
                (form.funcao.data == '' or Outros.funcao == form.funcao.data),
                (form.formacao.data == '' or Outros.formacao == form.formacao.data)
            ).all()
            return render_template("listar_outro.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_outro.html", form=form)


@app.route("/filtrar-consultorio", methods=('GET', 'POST'))
def consultorio():
    form = FiltroConsultorio(csrf_enabled=False)
    if form.validate_on_submit():
        if form.criar.data:
            criar_consultorio(form.telefone.data, form.endereco.data,
                              form.nome.data)
            return redirect(url_for('home'))
        elif form.filtrar.data:
            lista = Consultorio.query.filter(
                (form.telefone.data == '' or Consultorio.telefone == form.telefone.data),
                (form.endereco.data == '' or Consultorio.endereco == form.endereco.data),
                (form.nome.data == '' or Consultorio.nome == form.nome.data)
            ).all()
            return render_template("listar_consultorio.html", lista=lista)
        else:
            return redirect(url_for('home'))
    return render_template("filtrar_consultorio.html", form=form)