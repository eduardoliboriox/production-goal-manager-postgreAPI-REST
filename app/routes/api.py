from flask import Blueprint, jsonify, request

from app.services import modelos_service, pcp_service

bp = Blueprint("api", __name__)


@bp.get("/modelos")
def listar_modelos():
    return jsonify(modelos_service.listar())


@bp.post("/modelos")
def cadastrar_modelo():
    dados = {
        "codigo": request.form.get("codigo", "").strip(),
        "cliente": request.form.get("cliente", "").strip(),
        "setor": request.form.get("setor", "").strip(),
        "linha": request.form.get("linha", "").strip(),
        "meta_padrao": request.form.get("meta_padrao", "").strip(),
        "tempo_montagem": request.form.get("tempo_montagem", "").strip() or None,
        "blank": request.form.get("blank", "").strip(),
        "fase": request.form.get("fase", "").strip(),
    }

    # validações básicas rápidas (mantém o service como fonte)
    if not dados["codigo"]:
        return jsonify({"sucesso": False, "mensagem": "Código não informado"}), 400
    if not dados["fase"]:
        return jsonify({"sucesso": False, "mensagem": "Fase não informada"}), 400
    if not dados["linha"]:
        return jsonify({"sucesso": False, "mensagem": "Linha não informada"}), 400

    resp = modelos_service.cadastrar_modelo(dados)
    status = 200 if resp.get("sucesso") else 400
    return jsonify(resp), status


@bp.put("/modelos")
def atualizar_modelo():
    dados = {
        "codigo": request.form.get("codigo", "").strip(),
        "fase": request.form.get("fase", "").strip(),
        "linha": request.form.get("linha", "").strip(),
        "meta_padrao": request.form.get("meta_padrao", "").strip(),
        "tempo_montagem": request.form.get("tempo_montagem", "").strip(),
        "blank": request.form.get("blank", "").strip(),
        "novo_codigo": request.form.get("novo_codigo", "").strip(),
    }

    if not dados["codigo"] or not dados["fase"] or not dados["linha"]:
        return jsonify({"sucesso": False, "mensagem": "Código, fase e linha são obrigatórios"}), 400

    resp = modelos_service.atualizar_modelo(dados)
    status = 200 if resp.get("sucesso") else 400
    return jsonify(resp), status


@bp.delete("/modelos")
def excluir_modelo():
    dados = {
        "codigo": request.form.get("codigo", "").strip(),
        "fase": request.form.get("fase", "").strip(),
        "linha": request.form.get("linha", "").strip(),
    }

    resp = modelos_service.excluir_modelo(dados)
    status = 200 if resp.get("sucesso") else 400
    return jsonify(resp), status


@bp.post("/modelos/calculo_rapido")
def calculo_rapido():
    meta_hora = request.form.get("meta_hora", "").strip()
    minutos = request.form.get("minutos", "").strip()
    blank = request.form.get("blank", "").strip() if "blank" in request.form else None

    try:
        meta_hora = float(meta_hora)
        minutos = int(minutos)
        blank_val = int(blank) if blank not in (None, "", "0") else None
    except Exception:
        return jsonify({"sucesso": False, "erro": "Valores inválidos"}), 400

    dados = modelos_service.calculo_rapido(meta_hora, minutos, blank_val)
    return jsonify({"sucesso": True, "dados": dados})


@bp.post("/smt/calcular_meta")
def smt_calcular_meta():
    tempo_montagem = request.form.get("tempo_montagem", "").strip()
    blank = request.form.get("blank", "").strip()

    resp = modelos_service.calcular_meta_smt(tempo_montagem, blank)
    return jsonify(resp)


@bp.post("/smt/calcular_tempo")
def smt_calcular_tempo():
    meta_hora = request.form.get("meta_hora", "").strip()
    blank = request.form.get("blank", "").strip()

    resp = modelos_service.calcular_tempo_smt_inverso(meta_hora, blank)
    return jsonify(resp)


@bp.post("/pcp/calcular")
def calcular_pcp():
    payload = request.get_json(silent=True) or {}

    try:
        total_op = int(payload.get("total_op", 0))
        produzido = int(payload.get("produzido", 0))
        meta_hora = float(payload.get("meta_hora", 0))
        blank = int(payload.get("blank", 0))
        hora_inicio = str(payload.get("hora_inicio", "")).strip()
        turnos = payload.get("turnos", []) or []
        refeicao = bool(payload.get("refeicao", False))
    except Exception:
        return jsonify({"erro": "Payload inválido"}), 400

    resp = pcp_service.calcular_pcp(
        total_op=total_op,
        produzido=produzido,
        hora_inicio=hora_inicio,
        meta_hora=meta_hora,
        blank=blank,
        turnos_aplicados=turnos,
        considerar_refeicao=refeicao,
    )
    return jsonify(resp)


@bp.post("/calcular_perda")
def calcular_perda():
    meta_hora = request.form.get("meta_hora", "").strip()
    producao_real = request.form.get("producao_real", "").strip()

    try:
        resp = modelos_service.calcular_perda_producao(meta_hora, producao_real)
        return jsonify(resp)
    except Exception:
        return jsonify({"erro": "Erro ao calcular perda"}), 400
