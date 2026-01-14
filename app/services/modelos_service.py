from app.repositories import modelos_repository

def listar_codigos():
    return modelos_repository.listar_codigos()

def listar_modelos():
    return modelos_repository.listar_modelos()

def cadastrar_modelo(dados):
    try:
        modelos_repository.inserir(dados)
        return {"sucesso": True, "mensagem": "Modelo cadastrado"}
    except Exception:
        return {"sucesso": False, "mensagem": "Código já existe"}

def calcular_meta(dados):
    meta = float(dados["meta_padrao"])
    pessoas_atual = int(dados["pessoas_atuais"])
    pessoas_padrao = int(dados["pessoas_padrao"])
    minutos = int(dados["minutos"])

    meta_ajustada = round(
        meta * (pessoas_atual / pessoas_padrao) * 0.85
    )

    qtd = round(meta_ajustada * (minutos / 60))

    return {
        "resultado": f"{minutos} min → {qtd} peças"
    }

def calcular_perda_producao(meta_hora, producao_real):
    meta_hora = float(meta_hora)
    producao_real = float(producao_real)

    if meta_hora <= 0:
        return {"erro": "Meta inválida"}

    if producao_real >= meta_hora:
        return {
            "tempo_perdido": "0 minutos e 00 segundos",
            "pecas_faltantes": 0
        }

    minutos_por_peca = 60 / meta_hora

    tempo_produzido = producao_real * minutos_por_peca
    tempo_perdido = 60 - tempo_produzido

    minutos = int(tempo_perdido)
    segundos = int(round((tempo_perdido - minutos) * 60))

    if segundos == 60:
        minutos += 1
        segundos = 0

    pecas_faltantes = int(meta_hora - producao_real)

    return {
        "tempo_perdido": f"{minutos} minutos e {segundos:02d} segundos",
        "pecas_faltantes": pecas_faltantes
    }


