from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from jsonlite import JsonQuerier, JsonTable
from typing import Optional
from models.restaurant_model import Restaurant
from dataclasses import asdict

restaurant_table = JsonTable("tables/restaurants.json", Restaurant)
restaurant_querier = JsonQuerier(restaurant_table)

# ---------------------------
# Funções para Restaurantes
# ---------------------------

@jwt_required()
def create_restaurant(name: str, email: str, password: str, primary_color: str = "000000", secondary_color: str = "000000") -> int:
    user_id = get_jwt_identity()

    rest = Restaurant(
        owner_id=user_id,
        name=name,
        email=email,
        primary_color=primary_color,
        secondary_color=secondary_color
    )
    rest.set_password(password)

    restaurant_id = restaurant_table.insert(rest)
    restaurant_table.flush()
    return restaurant_id


@jwt_required()
def get_my_restaurants() -> list[Restaurant]:
    user_id = get_jwt_identity()
    return restaurant_table.get_by("owner_id", user_id)


def get_restaurant_by_id(_id: int) -> Optional[Restaurant]:
    results = restaurant_table.get_by("_id", _id)
    return results

def get_restaurants(limit: int):
        all_restaurants = restaurant_table.get_all()
        list = []
        for rest in all_restaurants:
            list.append(asdict(rest))
        return list
    
@jwt_required()
def update_restaurant(_id: int, **kwargs) -> bool:
    user_id = get_jwt_identity()
    results = restaurant_table.get_by("_id", _id)
    if not results or results[0].owner_id != user_id:
        return False

    rest = results[0]
    for key, value in kwargs.items():
        if hasattr(rest, key):
            setattr(rest, key, value)

    rest.updated_at = datetime.utcnow().isoformat()
    return restaurant_table.update(_id, rest)


@jwt_required()
def delete_restaurant(_id: int) -> bool:
    user_id = get_jwt_identity()
    results = restaurant_table.get_by("_id", _id)
    if not results or results[0].owner_id != user_id:
        return False

    ok = restaurant_table.delete(_id)
    if ok:
        restaurant_table.flush()
    return ok
