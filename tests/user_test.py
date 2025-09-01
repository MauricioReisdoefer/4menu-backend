import pytest
from datetime import datetime, timedelta
from models.user_model import User 

# ---------------------------
# Teste 1: Criar usuário e checar hash da senha
# ---------------------------
def test_set_password_and_check():
    user = User(name="Alice", email="alice@example.com")
    user.set_password("senha123")
    
    assert user.password_hash != "senha123"  # deve estar hash
    assert user.check_password("senha123") is True
    assert user.check_password("senhaErrada") is False

# ---------------------------
# Teste 2: Verifica updated_at após set_password
# ---------------------------
def test_updated_at_changes():
    user = User(name="Bob")
    old_updated = user.updated_at
    
    # espera 1 segundo só pra garantir diferença
    user.set_password("novaSenha")
    assert user.updated_at != old_updated

# ---------------------------
# Teste 3: Criação automática de created_at
# ---------------------------
def test_created_at_default():
    user = User(name="Charlie")
    # verifica se created_at está no formato ISO
    datetime.fromisoformat(user.created_at)
    datetime.fromisoformat(user.updated_at)