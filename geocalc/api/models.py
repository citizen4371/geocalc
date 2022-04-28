from typing import List

from fastapi import Query, HTTPException
from pydantic import BaseModel

from geocalc.geometry import Rectangle


class IoURequest:
    explanation = ('should contain 4 float values in order: '
            'top-left x, top-left y, bottom-right x, bottom-right y')

    def __init__(
        self, 
        box1: List[float] = Query(
            ...,
            description=f'List of coordinates of the first bounding box, {explanation}',
            example='?box1=0.5&box1=1.5&box1=1.5&box1=0.5'), 
        box2: List[float] = Query(
            ..., 
            description=f'List of coordinates of the second bounding box, {explanation}',
            example='&box2=0.5&box2=1.5&box2=1.5&box2=0.5')
    ):
        if len(box1) != 4:
            raise HTTPException(status_code=422, detail=f'box1 {self.explanation}')
        
        if len(box2) != 4:
            raise HTTPException(status_code=422, detail=f'box2 {self.explanation}')
        
        try:
            self.box1 = Rectangle.from_tuple(tuple(box1))
        except ValueError as ex:
            raise HTTPException(status_code=422, detail=f'box1 {str(ex)}')

        try:
            self.box2 = Rectangle.from_tuple(tuple(box2))
        except ValueError as ex:
            raise HTTPException(status_code=422, detail=f'box2 {str(ex)}')

class IoUResponse(BaseModel):
    result: float
