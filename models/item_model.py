from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from fastjson_db import JsonTable, JsonQuerier, JsonModel

# ---------------------------
# Modelo da Seção
# ---------------------------
@dataclass
class Item(JsonModel):
    _id: Optional[int] = field(default=None)
    name: str = ""
    description: str = ""
    price: float = 0.00
    section_id: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

# ---------------------------
# Tabela JSON
# ---------------------------
item_table = JsonTable("tables/item.json", Item)
item_querier = JsonQuerier(item_table)