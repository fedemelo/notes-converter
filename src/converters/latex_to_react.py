from fastapi import UploadFile

from re import Match, compile, error, escape, DOTALL

from src.exceptions import RegexProcessingError, conversion_error_handler
from src.latex_tools.tex_reader import decode_file_to_string


@conversion_error_handler
async def convert_tex_to_react(file: UploadFile) -> str:
    tex_content = await decode_file_to_string(file)
    react_content = convert_latex_code_to_react(tex_content)
    return react_content


def convert_latex_code_to_react(tex_content: str) -> str:

    stages = {

        # Temporarily remove ref commands
        "removing \\ref commands": (
            r"\\ref\{(.+?)\}",
            ""),
        "removing \\autoref commands": (
            r"\\autoref\{(.+?)\}",
            ""),

        # Temporarily remove figures
        "removing figures": (
            regex_to_match_environment_content("figure"),
            ""),

        "removing \\noindent commands": (
            r"\\noindent\s?",
            ""),

        "changing \\bvec to its original form": (
            r"\\bvec\{(.+?)\}",
            r"\\boldsymbol{\\mathbf{\1}}"),
        "changing \\uvec to its original form": (
            regex_to_match_command_content("uvec"),
            r"\\bm{\\hat{\\mathbf{\1}}}"
        ),

        "changing \\abs to its original form": (
            regex_to_match_command_content("abs"),
            r"\\left| \1 \\right|"
        ),
        "changing \\set to its original form": (
            regex_to_match_command_content("set"),
            r"\\left\{ \1 \\right\}"
        ),

        "changing \\ran to its original form": (
            r"\\ran",
            r"\\mathrm{ran}"
        ),
        "changing \\dom to its original form": (
            r"\\dom",
            r"\\mathrm{dom}"
        ),
        "changing \\cod to its original form": (
            r"\\cod",
            r"\\mathrm{cod}"
        ),

        "changing \\defint to its original form": (
            r"\\defint\{(.*?)\}\[(.*?)\]\{(.*?)\}\{(.*?)\}",
            r"\\int_{\3}^{\4} \1 \: \\mathrm{d}\2"
        ),
        "changing \\der to its original form": (
            r"\\der\[(.*?)\]\[(.*?)\]",
            r"\\frac{\\mathrm{d}\1}{\\mathrm{d}\2}"
        ),

        "replacing real number set symbol": (
            r"\\mathbb\{R\}",
            r"\\R"),
        "replacing integer number set symbol": (
            r"\\mathbb\{Z\}",
            r"\\Z"),
        "replacing natural number set symbol": (
            r"\\mathbb\{N\}",
            r"\\N"),
        "replacing rational number set symbol": (
            r"\\mathbb\{Q\}",
            r"\\Q"),
        "replacing complex number set symbol": (
            r"\\mathbb\{C\}",
            r"\\C"),

        "replacing display math, $$, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\$\$", r"\$\$"),
            transform_block_math),
        "replacing inline math, $, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\$", r"\$"),
            transform_inline_math),
        "replacing display math, \\[, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\\\[", r"\\\]"),
            transform_block_math),
        "replacing inline math, \\(, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\\\(", r"\\\)"),
            transform_inline_math),
        "replacing block math within equation* environment": (
            regex_to_match_environment_content(r"equation*"),
            transform_block_math),
        "replacing block math within_gather* environment": (
            regex_to_match_environment_content(r"gather*"),
            transform_gather_block_math),
        "replacing block math within align* environment": (
            regex_to_match_environment_content(r"align*"),
            transform_align_block_math),

        "replacing parts by level 1 headers": (
            regex_to_match_command_content("part"),
            regex_to_put_content_in_html_tag("h1")),
        "replacing sections by level 2 headers": (
            regex_to_match_command_content("section"),
            regex_to_put_content_in_html_tag("h2")),
        "replacing subsections by level 3 headers": (
            regex_to_match_command_content("subsection"),
            regex_to_put_content_in_html_tag("h3")),
        "replacing subsubsections by level 4 headers": (
            regex_to_match_command_content("subsubsection"),
            regex_to_put_content_in_html_tag("h4")),

        "formatting bold text": (
            regex_to_match_command_content("textbf"),
            regex_to_put_content_in_html_tag("b")),
        "formatting italic text": (
            regex_to_match_command_content("textit"),
            regex_to_put_content_in_html_tag("i")),
        "formatting underlined text": (
            regex_to_match_command_content("underline"),
            regex_to_put_content_in_html_tag("u")),
        "formatting emphasized text": (
            regex_to_match_command_content("emph"),
            regex_to_put_content_in_html_tag("em")),

        "replacing list items": (
            r"\\item(.+?)\n",
            regex_to_put_content_in_html_tag("li")+"\n"),
        "replace itemize environment by ul tag": (
            regex_to_match_environment_content("itemize"),
            regex_to_put_content_in_html_tag("ul")),
        "replace enumerate environment by ol tag": (
            regex_to_match_environment_content("enumerate"),
            regex_to_put_content_in_html_tag("ol")),

        "replace tip environment by custom react component": (
            regex_to_match_environment_content("tip"),
            regex_to_put_content_in_html_tag("Tip")),

        "converting latex comments to html comments": (
            r"%([^\n]*?)(\n)",
            r"{/* \1 */}"),
    }

    for stage, pattern in stages.items():
        regex, replacement = pattern
        try:
            tex_content = compile(regex).sub(replacement, tex_content)
            print(stage[0].upper() + stage[1:])
        except error as e:
            raise RegexProcessingError(stage, pattern, str(e))
    return tex_content


def transform_block_math(match: Match) -> str:
    """Escape backslashes and enclose in my custom react LaTeX block component"""
    content = match.group(1).replace("\\", "\\\\")
    # TODO: Improve this function to recognize simple math and use <M block> component instead of <LaTeX block>
    return "<LaTeX block>{`"+content+"`}</LaTeX>"


def transform_gather_block_math(match: Match) -> str:
    content = match.group(1).replace("\\\\", "").replace("\\", "\\\\")
    re_add_gather = r"\\begin{gather*}"+content+r"\\end{gather*}"
    return "<LaTeX block>{`"+re_add_gather+"`}</LaTeX>"


def transform_align_block_math(match: Match) -> str:
    content = match.group(1).replace("\\\\", "").replace("\\", "\\\\")
    re_add_align = r"\\begin{align*}"+content+r"\\end{align*}"
    return "<LaTeX block>{`"+re_add_align+"`}</LaTeX>"


def transform_inline_math(match: Match) -> str:
    """Escape backslashes and enclose in my custom react LaTeX inline component"""
    # TODO: Improve this function to recognize simple math and use <M> component instead of <LaTeX>
    content = match.group(1).replace("\\", "\\\\")
    return "<LaTeX>{`"+content+"`}</LaTeX>"


def regex_to_match_between_delimiters(bgin_delimiter: str, end_delimiter: str) -> str:
    """Recieves a delimiter and returns a regex to match content between two delimiters.
        If a delimiter is a special character in regex, it must be escaped. E.g: $ -> \$
    """
    # Caveat:

    # As the match is non-greedy, it will match the shortest possible content between the delimiters.
    # That means that if the end_delimiter character appears in the content, the match will end
    # at its first occurrence, which in most cases is not the desired behavior.

    # That could be fixed by doing a proper parsing of the content, but that would be a much more
    # complex solution, and given that this is much of a specific use case, I don't think it's worth the effort.
    return bgin_delimiter + r"(.+?)" + end_delimiter


def regex_to_match_command_content(command: str) -> str:
    """Recieves a command and returns a regex to match content between curly braces after the
            command."""
    # Same caveat as the previous function: if the content contains the closing curly brace, the match will end
    # at its first occurrence, which is not the desired behavior.
    return r"\\" + command + r"\{(.+?)\}"


def regex_to_match_environment_content(environment: str) -> str:
    """Receives an environment and returns a regex to match content between the begin and end of the
       environment, including content that spans multiple lines."""
    pattern = r"\\begin\{" + escape(environment) + \
        r"\}(.+?)\\end\{" + escape(environment) + r"\}"
    return compile(pattern, DOTALL)


def regex_to_put_content_in_html_tag(tag: str) -> str:
    """Recieves an html tag and returns a regex to put the matched content inside the tag."""
    return "<" + tag + r">\1</" + tag + ">"
