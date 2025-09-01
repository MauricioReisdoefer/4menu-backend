from dataclasses import asdict
from models.item_model import Item, item_table, item_querier
from flask import jsonify

# ---------------------------
# Criar Item
# ---------------------------
def criar_item(name: str, description: str, price: float, section_id: int) -> Item:
    novo_item = Item(
        name=name,
        description=description,
        price=price,
        section_id=section_id
    )
    item_table.insert(novo_item)
    return novo_item

# ---------------------------
# Deletar Item
# ---------------------------
def deletar_item(item_id: int) -> bool:
    item = item_querier.get_by("_id", item_id)
    if not item:
        return False
    item_table.delete(item[0])
    return True

def get_item(secao_id: int):
    itens = item_querier.filter(section_id=secao_id)  # melhor usar 'filter' se suportado
    lista = [asdict(item) for item in itens]

    if lista:  # lista não vazia
        return jsonify(lista), 200
    else:  # lista vazia
        return jsonify({"message": "Nenhum item encontrado"}), 404