from flask import Blueprint, flash, request, jsonify
from flask import redirect, render_template, url_for
from forms import MapListForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

MapsModule = Blueprint("MapsModule", __name__)


@MapsModule.route("/MapsList", methods=['GET', 'POST'])
def seeMapList():
    form = MapListForm()
    active_user = current_user

    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]

    data = [
            ['1', 'ferdinade', '22-54-2244'],
            ['2', 'alo', '24-54-2244'],
            ['3', 'bread', '4-54-2244'],
            ['4', 'pão', '25-54-2244']
        ]

    return render_template("ListagemMapas.html", title = "MapList", formFront = form, active_user = employee, data = data)

@MapsModule.route("/FilteredList", methods=['GET', 'POST'])
def FilteredList():
    value = request.form.get('value')

    # Processar os dados correspondentes com base no valor recebido

    # Exemplo: retornar uma lista de dados
    data = [
        ['Nome 1', 'Descrição 1'],
        ['Nome 2', 'Descrição 2']
    ]

    return jsonify(data)

@MapsModule.route("/MakeMap", methods=['GET', 'POST'])
def CreateStoreMap():

    return render_template("CriarMapa.html", title = "MakeStoreMap")



@MapsModule.route("/EditMap", methods=['GET', 'POST'])
def AlterStoreMap():

    return render_template("EditarMapa.html", title = "EditStoreMap")