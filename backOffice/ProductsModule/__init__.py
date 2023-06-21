from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

ProductsModule = Blueprint("ProductsModule", __name__)


@ProductsModule.route("/ProductsList", methods=['GET', 'POST'])
def seeProductList():

    return render_template("ListagemProdutos.html", title = "MapList")