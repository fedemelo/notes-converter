from fastapi import UploadFile

from src.exceptions import conversion_error_handler
from src.latex_tools.tex_reader import decode_file_to_string
from src.parsers.latex.latex import LatexParser
from src.renderers.react import ReactRenderer


@conversion_error_handler
async def convert_tex_to_react(file: UploadFile) -> str:
    tex_content = await decode_file_to_string(file)
    return convert_latex_code_to_react(tex_content)


def convert_latex_code_to_react(tex_content: str) -> str:
    doc = LatexParser().parse(tex_content)
    return ReactRenderer().render(doc)
