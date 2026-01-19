from flask import Blueprint, render_template, request
from app.services.modelos_service import listar_codigos, calcular_perda_producao, resumo_dashboard

bp = Blueprint("pages", __name__)

@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    dados = resumo_dashboard()
    return render_template("dashboard.html", **dados)

@bp.route("/cadastro")
def cadastro():
    try:
        codigos = listar_codigos()
    except Exception:
        codigos = []
    return render_template("cadastro.html", codigos=codigos)

@bp.route("/modelos")
def modelos():
    return render_template("modelos.html", codigos=listar_codigos())

@bp.route("/calculo")
def calculo():
    return render_template("calcular.html", codigos=listar_codigos())

@bp.route("/perdas", methods=["GET", "POST"])
def perdas():
    resultado = None

    if request.method == "POST":
        meta_hora = request.form.get("meta_hora")
        producao = request.form.get("producao")

        resultado = calcular_perda_producao(meta_hora, producao)

    return render_template("perdas.html", resultado=resultado)
