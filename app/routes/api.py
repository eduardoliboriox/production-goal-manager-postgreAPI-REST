from flask import Blueprint, request, jsonify
from app.services import modelos_service
from app.services.modelos_service import calcular_perda_producao

bp = Blueprint("api", __name__)

@bp.route("/modelos", methods=["GET"])
def listar():
    return jsonify({"data": modelos_service.listar_modelos()})

@bp.route("/modelos", methods=["POST"])
def cadastrar():
    dados = request.form
    return jsonify(modelos_service.cadastrar_modelo(dados))

@bp.route("/modelos/calcular", methods=["POST"])
def calcular_meta():
    return jsonify(modelos_service.calcular_meta(request.form))

@bp.route("/calcular_perda", methods=["POST"])
def calcular_perda():
    meta_hora = float(request.form.get("meta_hora"))
    producao_real = float(request.form.get("producao_real"))

    resultado = calcular_perda_producao(meta_hora, producao_real)

    return jsonify(resultado)



