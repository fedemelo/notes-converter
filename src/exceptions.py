from fastapi import HTTPException


class FileProcessingError(Exception):
    def __init__(self, operation, file, detail):
        self.operation = operation
        self.detail = detail
        super().__init__(f"Error while {operation} file {file}: {detail}")


class RegexProcessingError(Exception):
    def __init__(self, stage, pattern, detail):
        self.pattern = pattern
        self.detail = detail
        super().__init__(f"Error when {stage}, processing regex {pattern}: {detail}")


class MalformedLatexError(Exception):
    # No Python library does LaTeX structural validation well, and running the
    # LaTeX compiler as a validator is not viable because inputs are fragments,
    # not compilable documents. Instead, the parser raises this on known
    # structural violations (e.g. \item outside a list) as it encounters them.
    pass


def conversion_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileProcessingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RegexProcessingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except MalformedLatexError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return wrapper
