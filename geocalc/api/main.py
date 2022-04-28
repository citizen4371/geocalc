from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from geocalc.api.models import IoURequest, IoUResponse

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Welcome to the IoU calculator'}


@app.get('/calculations/iou', response_model=IoUResponse)
async def iou(request: IoURequest = Depends()):
    result = round(request.box1.iou(request.box2), 3)

    return JSONResponse({'result': result}, headers={'Cache-Control': 'max-age=86400'})