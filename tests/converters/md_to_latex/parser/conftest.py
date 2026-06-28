import pytest

from src.converters.md_to_latex.parsers.obsidian import ObsidianMarkdownParser


@pytest.fixture
def parser():
    return ObsidianMarkdownParser()
