from flask import render_template, redirect, url_for
from src import app
from src.forms import *
from src.models import *
import os

@app.route("/", methods=('GET', 'POST'))
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
        os.system('clear')
        # Iniciar tabelas
        db.create_all()
        for table in db.metadata.sorted_tables:
            db.session.execute(table.delete())
        db.session.commit()

        # Criação de Plano de Saúde
        db.session.add(
            PlanoDeSaude(cnpj='12345678901234',
                         nome_da_empresa='Porto Seguro',
                         telefone='(11)3012-4561',
                         email='porto@porto.com',
                         site='portoseguro.com.br')
        )
        db.session.commit()
        for a in PlanoDeSaude.query.all(): print(a)

        # Criação de Paciente
        paciente = Paciente(cpf='12345678901',
                            nome='Fernando da Silva',
                            email='fernando.silva@gmail.com',
                            telefone='(14)5124-1563',
                            endereco='Avenida dos Pacientes, 215',
                            data_de_nascimento='12/05/1997',
                            sexo='masculino',
                            historico='alergias diversas',
                            plano_de_saude_cnpj='12345678901234')
        db.session.add(paciente)
        db.session.commit()
        for a in Paciente.query.all(): print(a)

        # Criação de Funcionário, Médico e Assistente
        funcionario = Funcionario(cpf='11111111111',
                                  nome='Paulo Cezar',
                                  email='paulo@cezar.com',
                                  telefone='(11) 1234-5678',
                                  endereco='Rua dos Funcionarios, 12',
                                  formacao='',
                                  salario='R$999999,00',
                                  periodo_de_trabalho='diurno')
        db.session.add(funcionario)
        db.session.commit()

        medico = Medico(cpf='22222222222',
                        nome='Dr. Rodrigo Mall',
                        email='rodrigo@yahoo.com.br',
                        telefone='(22)1234-1234',
                        endereco='Bosque dos Medicos, 34 - apto 3',
                        formacao='Faculdade de Medicina',
                        salario='R$12,00',
                        periodo_de_trabalho='noturno',
                        crm='12345-6',
                        especialidades='cirurgião')
        db.session.add(medico)
        db.session.commit()

        assistente = Assistente(cpf='33333333333',
                                nome='Pedro Arantes',
                                email='pedro@gmail.com',
                                telefone='(23)1234-5555',
                                endereco='Boulevard Assistencial, 7000',
                                formacao='Enfermagem',
                                salario='R$5,00',
                                periodo_de_trabalho='Integral',
                                funcao='Enfermeiro, Massagista')
        db.session.add(assistente)
        db.session.commit()

        db.session.add(funcionario)
        db.session.commit()
        for a in Funcionario.query.all(): print(a)

        return('Sucesso')
    except Exception as e:
        raise e
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