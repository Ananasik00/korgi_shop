import requests

random_dog_url = 'http://localhost:8001'
dog_image_url = f'{random_dog_url}/dog'
dog_image_by_breed_url = f'{random_dog_url}/dog_by_breed'

def test_5_get_random_dog_image():
    res = requests.get(dog_image_url)
    assert res.status_code == 200
    assert "image_url" in res.json()

def test_6_get_corgi_image():
    res = requests.get(f"{dog_image_by_breed_url}?breed=corgi")
    assert res.status_code == 200
    assert "image_url" in res.json()
