import requests

korgi_shop_url = 'http://localhost:8000'
add_korgi_url = f'{korgi_shop_url}/add_korgi'
get_korgis_url = f'{korgi_shop_url}/korgis'
get_korgi_by_id_url = f'{korgi_shop_url}/get_korgi_by_id'
delete_korgi_url = f'{korgi_shop_url}/delete_korgi'

new_korgi = {
    "id": 99,
    "name": "Coco",
    "age": 2,
    "description": "A lovely corgi",
    "price": 500
}

def test_1_add_korgi():
    res = requests.post(add_korgi_url, json=new_korgi)
    assert res.status_code == 200

def test_2_get_korgis():
    res = requests.get(get_korgis_url).json()
    assert any(korgi['name'] == "Coco" for korgi in res)

def test_3_get_korgi_by_id():
    res = requests.get(get_korgis_url).json()
    korgi_id = next((korgi['id'] for korgi in res if korgi['name'] == "Coco"), None)
    res = requests.get(f"{get_korgi_by_id_url}?korgi_id={korgi_id}").json()
    assert res['id'] == korgi_id

def test_4_delete_korgi():
    res = requests.get(get_korgis_url).json()
    korgi_id = next((korgi['id'] for korgi in res if korgi['name'] == "Coco"), None)
    res = requests.delete(f"{delete_korgi_url}?korgi_id={korgi_id}")
    assert res.status_code == 200
