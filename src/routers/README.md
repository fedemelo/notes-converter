# Routers

Routers are built so that adding a conversion doesn't require creating a new router.

There's a generic router factory that generates the two endpoints for any conversion:
- `POST /{name}/convert-file` — upload a source file, receive the converted file as a download
- `POST /{name}/convert-text` — send plain text, receive `{"result": "..."}` JSON

To add a conversion, implement `converter(source: str) -> str` anywhere under `src/converters/` and add a `Conversion(...)` entry to the `registry.py`.
