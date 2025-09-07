from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from fastjson_db import JsonTable, JsonQuerier, JsonModel

# ---------------------------
# Modelo da Seção
# ---------------------------
@dataclass
class Secao(JsonModel):
    _id: Optional[int] = field(default=None)
    title: str = ""
    restaurant_id: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

# ---------------------------
# Tabela JSON
# ---------------------------
secao_table = JsonTable("tables/secao.json", Secao)
secao_querier = JsonQuerier(secao_table)