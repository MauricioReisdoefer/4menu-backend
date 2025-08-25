from models.menu_model import MenuModel
from db import db

# Criar um menu
def create_menu(name: str, restaurant_id: int) -> MenuModel:
    new_menu = MenuModel(name=name, restaurant_id=restaurant_id)
    db.session.add(new_menu)
    db.session.commit()
    return new_menu


# Buscar todos os menus
def get_all_menus() -> list[MenuModel]:
    return MenuModel.query.all()

# Buscar um menu por id
def get_menu_by_id(menu_id: int) -> MenuModel | None:
    return MenuModel.query.get(menu_id)

# Atualizar um menu
def update_menu(menu_id: int, name: str = None, restaurant_id: int = None) -> MenuModel | None:
    menu = MenuModel.query.get(menu_id)
    if not menu:
        return None
    if name:
        menu.name = name
    if restaurant_id:
        menu.restaurant_id = restaurant_id
    db.session.commit()
    return menu

# Deletar um menu
def delete_menu(menu_id: int) -> bool:
    menu = MenuModel.query.get(menu_id)
    if not menu:
        return False
    db.session.delete(menu)
    db.session.commit()
    return True
