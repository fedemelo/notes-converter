from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from src.converters.md_to_latex import convert_md_to_latex

router = APIRouter(
    prefix="/md-to-latex",
    tags=["md-to-latex"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/convert_md_file_to_latex", status_code=status.HTTP_200_OK)
async def convert_md_file_to_latex(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="File must have a .md extension")
    raw = await file.read()
    try:
        latex = convert_md_to_latex(raw.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"latex": latex})


@router.post("/convert_md_text_to_latex", status_code=status.HTTP_200_OK)
async def convert_md_text_to_latex(
    md_content: str = Body(
        ..., description="Obsidian Markdown as plain text", media_type="text/plain"
    ),
):
    try:
        latex = convert_md_to_latex(md_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"latex": latex})
