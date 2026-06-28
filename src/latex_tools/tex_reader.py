from fastapi import UploadFile

from src.exceptions import FileProcessingError, conversion_error_handler


@conversion_error_handler
async def decode_file_to_string(file: UploadFile):
    try:
        content = await file.read()
        return content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise FileProcessingError("decoding", file.filename, str(e))
    except IOError as e:
        raise FileProcessingError("reading file", file.filename, str(e))
