from fastapi import APIRouter, HTTPException, Query, status, File, UploadFile
from fastapi.responses import FileResponse
from src.converters.latex_to_react import convert_tex_to_react
from src.persistence.persistence import persist_content
from src.latex_tools.tex_analyzer import replace_command_with_delimiters


router = APIRouter(
    prefix="/latex",
    tags=["latex"],
    responses={404: {"detail": "Not found"}}
)


@router.post("/convert_to_react", status_code=status.HTTP_201_CREATED)
async def convert_to_react(file: UploadFile = File(...)):
    _check_file_extension(file.filename, ".tex")
    converted_content = await convert_tex_to_react(file)
    path = persist_content(file.filename, converted_content)
    return FileResponse(path=path, filename=file.filename.split(".")[0] + ".txt", media_type="text/plain")


@router.post("/change_command_to_delimiters", status_code=status.HTTP_201_CREATED)
async def change_command_to_delimiters(file: UploadFile = File(...), command: str = Query(..., description="Command"), left_delimiter: str = Query(..., description="Left delimiter"), right_delimiter: str = Query(..., description="Right delimiter")):
    _check_file_extension(file.filename, ".tex")
    tex_content = await replace_command_with_delimiters(file, command, left_delimiter, right_delimiter)
    filename = file.filename.split(".")[0] + f"_without_{command}.tex"
    path = persist_content(filename, tex_content)
    return FileResponse(path=path, filename=filename, media_type="text/plain")


def _check_file_extension(filename: str, expected_extension: str):
    if not filename.endswith(expected_extension):
        raise HTTPException(status_code=400, detail=f"File must have a {expected_extension} extension")
    return