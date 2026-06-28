import pytest

from src.converters.md_to_latex.renderers.latex import LatexRenderer


@pytest.fixture
def renderer():
    return LatexRenderer()
