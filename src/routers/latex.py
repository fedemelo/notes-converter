from os import path
from fastapi import APIRouter, HTTPException, Query, status
from fastapi import FastAPI, File, UploadFile
from src.converters.latex_to_react import convert_latex_to_react


router = APIRouter(
    prefix="/latex",
    tags=["latex"],
    responses={404: {"detail": "Not found"}}
)


@router.post("/convert_to_react", status_code=status.HTTP_201_CREATED)
async def convert_to_react(file: UploadFile = File(...)):
    filename = file.filename
    if file.filename.endswith(".tex"):
        with open(file.filename, "wb") as f:
            convert_latex_to_react(f)
    else:
        raise HTTPException(status_code=400, detail="File must be a .tex file")
    return {"filename": file.filename}