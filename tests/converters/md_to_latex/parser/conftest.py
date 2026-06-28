import pytest

from src.parsers.markdown.obsidian import ObsidianMarkdownParser


@pytest.fixture
def parser():
    return ObsidianMarkdownParser()
