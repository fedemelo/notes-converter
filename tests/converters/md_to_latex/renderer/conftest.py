import pytest

from src.renderers.latex import LatexRenderer


@pytest.fixture
def renderer():
    return LatexRenderer()
