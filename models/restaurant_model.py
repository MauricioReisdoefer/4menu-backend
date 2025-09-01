from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from jsonlite import JsonTable, JsonQuerier

# ---------------------------
# Modelo de Restaurante
# ---------------------------
@dataclass
class Restaurant:
    _id: Optional[int] = field(default=None)
    owner_id: int = 0
    layout: int = 0
    name: str = ""
    email: str = ""
    primary_color: str = "000000"
    secondary_color: str = "000000"
    password_hash: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
        self.updated_at = datetime.utcnow().isoformat()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
# ---------------------------
# Tabela JSON
# ---------------------------
restaurant_table = JsonTable("tables/restaurants.json", Restaurant)
restaurant_querier = JsonQuerier(restaurant_table)