from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
#from schemas.review_schema import Review, ReviewCreate
#from crud.review_crud import 
from api.dependencies import get_db

router = APIRouter()



