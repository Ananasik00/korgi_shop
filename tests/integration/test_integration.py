import asyncpg
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'random_dog_service/app'))
sys.path.append(str(BASE_DIR / 'korgi_shop_service/app'))

from random_dog_service.app.main import service_alive as random_dog_status
from korgi_shop_service.app.main import service_alive as korgi_shop_status

@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect('postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query')
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

@pytest.mark.asyncio
async def test_random_dog_service_connection():
    r = await random_dog_status()
    assert r == {'message': 'Service alive'}

@pytest.mark.asyncio
async def test_korgi_shop_service_connection():
    r = await korgi_shop_status()
    assert r == {'message': 'Service alive'}
