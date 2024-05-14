from os import path

from fastapi import HTTPException

def persist_content(filename: str, content: str) -> str:
    try:
        converted_file_path = path.join(path.dirname(__file__), "converted_files", filename.split(".")[0] + ".txt")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating the file path to persist file {filename}: {e}")
    
    try:
        with open(converted_file_path, "w") as f:
            f.write(content)
            f.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error persisting the converted content to path {converted_file_path}: {e}")
    
    return converted_file_path