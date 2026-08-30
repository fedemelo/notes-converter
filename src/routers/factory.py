import inspect
from enum import Enum

from fastapi import APIRouter, Body, File, HTTPException, Query, UploadFile, status
from fastapi.responses import PlainTextResponse, Response

from src.routers.conversion import Conversion


def _plain_values(options: dict) -> dict:
    """Unwraps Enum-typed option values to their plain string value for the converter."""
    return {k: v.value if isinstance(v, Enum) else v for k, v in options.items()}


def _option_parameters(conversion: Conversion) -> list[inspect.Parameter]:
    """Builds the extra keyword-only signature parameters for a conversion's options."""
    return [
        inspect.Parameter(
            option.name,
            inspect.Parameter.KEYWORD_ONLY,
            default=Query(option.default, description=option.description),
            annotation=option.choices or str,
        )
        for option in conversion.options
    ]


def make_conversion_router(conversion: Conversion) -> APIRouter:
    router = APIRouter(
        prefix=f"/{conversion.endpoint_name}",
        tags=[conversion.tag_name],
        responses={404: {"detail": "Not found"}},
    )

    @router.post(
        "/convert-file",
        status_code=status.HTTP_200_OK,
        response_class=Response,
    )
    async def convert_file(file: UploadFile = File(...), **options):
        if not file.filename or not file.filename.endswith(
            f".{conversion.source_extension}"
        ):
            raise HTTPException(
                status_code=400,
                detail=f"File must have a .{conversion.source_extension} extension",
            )
        try:
            raw = await file.read()
            source = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Could not decode file as UTF-8: {e}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
        try:
            result = conversion.converter(source, **_plain_values(options))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        stem = file.filename.rsplit(".", 1)[0]
        return Response(
            content=result,
            media_type="text/plain",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{stem}.{conversion.target_extension}"'
                )
            },
        )

    convert_file.__signature__ = inspect.Signature(
        [
            inspect.Parameter(
                "file",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=File(...),
                annotation=UploadFile,
            ),
            *_option_parameters(conversion),
        ]
    )

    @router.post(
        "/convert-text",
        status_code=status.HTTP_200_OK,
        response_class=PlainTextResponse,
    )
    async def convert_text(content: str = Body(...), **options):
        try:
            return conversion.converter(content, **_plain_values(options))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    convert_text.__signature__ = inspect.Signature(
        [
            inspect.Parameter(
                "content",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Body(
                    ...,
                    description=f"{conversion.source_format} content as plain text",
                    media_type="text/plain",
                ),
                annotation=str,
            ),
            *_option_parameters(conversion),
        ]
    )

    return router
