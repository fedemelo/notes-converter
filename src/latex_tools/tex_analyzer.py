from src.latex_tools.tex_reader import decode_file_to_string
from src.exceptions import conversion_error_handler
from fastapi import UploadFile


@conversion_error_handler
async def replace_command_with_delimiters(
    file: UploadFile,
    command: str,
    left_delimiter: str,
    right_delimiter: str
) -> str:
    tex_content = await decode_file_to_string(file)
    tex_content = replace_command_with_delimiters_by_counting_brackets(
        tex_content, command, left_delimiter, right_delimiter)
    return tex_content


def replace_command_with_delimiters_by_counting_brackets(
    tex_content: str,
    command: str,
    left_delimiter: str,
    right_delimiter: str
) -> str:
    """
    This function replaces each instance of a command with delimiters.

    It uses a (theoretical) stack (a counter) to keep track of the number of opening and closing brackets.
    When the stack is empty, the function knows that it has found the closing bracket of the command.

    This replacement can't be done with a simple regex because the command's argument can contain nested brackets.
    """
    new_content = ""

    stack = 0
    is_stacking = False

    i = 0

    while i < len(tex_content):

        if tex_content[i:i + len(command)] == command:
            is_stacking = True
            i += len(command)
            continue  # Don't add the command to the new content

        if is_stacking:
            if tex_content[i] == "{":
                stack += 1

                if stack == 1:
                    new_content += left_delimiter

                    i += 1
                    continue    # Don't add the opening bracket of the command to the new content
            elif tex_content[i] == "}":
                stack -= 1

                if stack == 0:
                    is_stacking = False
                    new_content += right_delimiter

                    i += 1
                    continue  # Don't add the closing bracket of the command to the new content

        new_content += tex_content[i]
        i += 1

    if stack != 0:
        raise ValueError(
            f"Unbalanced brackets in the command {command}. The stack is {stack}."
        )

    return new_content
