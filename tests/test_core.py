import justext


def test_words_should_be_split_by_br_tag():
    paragraphs = justext.justext('abc<br/>def becoming abcdef', justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["abc def becoming abcdef"]


ARTICLE_PARAGRAPH = "<p>%s</p>" % (
    "The council voted on Tuesday to approve the new budget for the city. " * 3)


def test_nav_is_removed():
    html = ("<article><nav><h2>Contents</h2><ul><li><a href='#budget'>Budget</a>"
        "</li></ul></nav>" + ARTICLE_PARAGRAPH * 2 + "</article>")

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    # the short heading of the table of contents used to be kept as good text
    assert "Contents" not in [p.text for p in paragraphs]
