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


def conversion_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileProcessingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RegexProcessingError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return wrapper