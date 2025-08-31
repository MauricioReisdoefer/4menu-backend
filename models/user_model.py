from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from jsonlite import JsonTable, JsonQuerier

# ---------------------------
# Modelo de Usuário
# ---------------------------
@dataclass
class User:
    _id: Optional[int] = field(default=None)
    name: str = ""
    email: str = ""
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
user_table = JsonTable("users.json", User)
user_querier = JsonQuerier(user_table)