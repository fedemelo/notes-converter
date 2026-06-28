from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from src.routers.conversion import Conversion


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
    async def convert_file(file: UploadFile = File(...)):
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
            result = conversion.converter(source)
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

    @router.post(
        "/convert-text",
        status_code=status.HTTP_200_OK,
        response_class=PlainTextResponse,
    )
    async def convert_text(
        content: str = Body(
            ...,
            description=f"{conversion.source_format} content as plain text",
            media_type="text/plain",
        ),
    ):
        try:
            return conversion.converter(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
