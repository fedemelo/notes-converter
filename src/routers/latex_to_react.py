from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from src.converters.latex_to_react.latex_to_react import (
    convert_latex_code_to_react,
    convert_tex_to_react,
)
from src.persistence.persistence import persist_content

router = APIRouter(
    prefix="/latex", tags=["latex"], responses={404: {"detail": "Not found"}}
)

@router.post("/convert_tex_file_to_react", status_code=status.HTTP_201_CREATED)
async def convert_tex_file_to_react(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if not file.filename or not file.filename.endswith(".tex"):
        raise HTTPException(status_code=400, detail="File must have a .tex extension")

    converted_content = await convert_tex_to_react(file)
    path = persist_content(file.filename, converted_content)
    return FileResponse(
        path=path,
        filename=file.filename.split(".")[0] + ".txt",
        media_type="text/plain",
    )


@router.post("/convert_tex_text_to_react", status_code=status.HTTP_200_OK)
async def convert_tex_text_to_react(
    tex_content: str = Body(
        ..., description="LaTeX content as plain text", media_type="text/plain"
    )
):
    try:
        react_content = convert_latex_code_to_react(tex_content)
        output_file_path = "converted_output.txt"
        with open(output_file_path, "w") as output_file:
            output_file.write(react_content)
        return JSONResponse(
            content={"message": "Conversion successful", "file_path": output_file_path}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
