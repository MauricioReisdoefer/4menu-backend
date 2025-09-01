from dataclasses import asdict
from models.secao_model import Secao, secao_table, secao_querier
# ---------------------------
# Criar Seção
# ---------------------------
def criar_secao(title: str, restaurant_id: int) -> Secao:
    nova_secao = Secao(title=title, restaurant_id=restaurant_id)
    secao_table.insert(nova_secao)
    return nova_secao

# ---------------------------
# Deletar Seção
# ---------------------------
def deletar_secao(secao_id: int) -> bool:
    secao = secao_querier.get_by("_id", secao_id)
    if not secao:
        return False
    secao_table.delete(secao[0])
    return True

def get_secao(rest_id: int):
    secoes = secao_querier.filter(restaurant_id=rest_id)
    lista = []
    for section in secoes:
        lista.append(asdict(section))
    return secoes