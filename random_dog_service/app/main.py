import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.get("/dog")
async def get_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"image_url": data['message']}
    else:
        raise HTTPException(status_code=400, detail="Error retrieving data from Dog API")


@app.get("/dog_by_breed")
async def get_dog_image_by_breed(breed: str):
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"image_url": data['message']}
    else:
        raise HTTPException(status_code=400, detail="Error retrieving data or breed not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
