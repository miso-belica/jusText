import pytest

from justext.core import PathInfo, revise_paragraph_classification
from justext.paragraph import Paragraph


def p(class_):
    paragraph = Paragraph(PathInfo())
    paragraph.heading = False
    paragraph.cf_class = class_
    return paragraph


def test_no_paragraphs_are_revised_to_no_paragraphs():
    paragraphs = []
    revise_paragraph_classification(paragraphs)

    assert paragraphs == []


@pytest.mark.parametrize("class_", ["short", "neargood", "bad"])
def test_single_bad_paragraph(class_):
    paragraphs = [p(class_)]
    revise_paragraph_classification(paragraphs)

    assert paragraphs[0].class_type == "bad"


def test_single_good_paragraph():
    paragraphs = [p("good")]
    revise_paragraph_classification(paragraphs)

    assert paragraphs[0].class_type == "good"


@pytest.mark.parametrize("prev, result_class", [
    ([p("good")], "good"),
    ([p("neargood")], "good"),
    ([p("bad")], "bad"),
    ([p("short")], "bad"),
])
def test_paragraph_with_prev_paragraphs(prev, result_class):
    paragraphs = [*prev, p("short")]
    revise_paragraph_classification(paragraphs)

    assert paragraphs[0].class_type == result_class
