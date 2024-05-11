# LaTeX to React

Repo featuring a simple API to convert my LaTeX undergraduate notes to React components, to by displayed in my [personal website](https://fedemelo.github.io/apuntes/).

It has many features of a generic LaTeX to HTML converter, but it is tailored to my notes' structure. Particularly, it is able to convert theorems, definitions, examples, and other custom LaTeX environments I designed at the time to equivalent React components.

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

   The server will be running on `http://localhost:8000`.
