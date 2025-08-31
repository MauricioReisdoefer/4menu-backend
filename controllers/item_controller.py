from models.item_model import Item, item_table, item_querier

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
