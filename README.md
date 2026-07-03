# Notes Converter

API to convert between note formats. Currently supports:

- **Obsidian Markdown → LaTeX**: Converts Obsidian Markdown files to LaTeX, tailored to my notes' structure.
- **LaTeX → React JSX**: Converts LaTeX to React components for display on my [personal website](https://fedemelo.github.io/apuntes/). Handles custom LaTeX environments (theorems, definitions, examples, etc.) that I designed for my undergraduate notes.
- **TeX `$`/`$$` delimiters → LaTeX `\(`/`\[` delimiters**: Normalizes math delimiters in LaTeX files.

## Setup Instructions

The project must be run using [Python 3.11.9](https://www.python.org/downloads/release/python-3119/).

1. Create a virtual environment

   ```shell
   python -m venv venv
   ```

2. Activate the virtual environment

   Unix:

   ```shell
   source venv/bin/activate
   ```

   Windows:

   ```batch
   venv\Scripts\activate.bat
   ```

3. Install dependencies

   ```shell
   pip install -r requirements.txt
   ```

4. Run the server. In the root of the project, run the following command:

   ```shell
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or with `make`:

   ```shell
   make run
   ```

   The server will be running on `http://localhost:8000`.
