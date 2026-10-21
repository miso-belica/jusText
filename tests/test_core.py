import justext


def test_words_should_be_split_by_br_tag():
    paragraphs = justext.justext('abc<br/>def becoming abcdef', justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["abc def becoming abcdef"]


ARTICLE_PARAGRAPH = "<p>%s</p>" % (
    "The council voted on Tuesday to approve the new budget for the city. " * 3)


def test_footer_is_removed():
    html = (ARTICLE_PARAGRAPH * 2 + "<footer><p>We use cookies to make sure that"
        " we give you the best experience on our website. If you continue to use"
        " this site we will assume that you are happy with it.</p></footer>")

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    assert [p.text for p in paragraphs if "cookies" in p.text] == []


def test_footer_with_quote_attribution_is_kept():
    html = (ARTICLE_PARAGRAPH + "<blockquote><p>We are going to invest in the"
        " future of all of our children.</p><footer>Mayor Jane Smith</footer>"
        "</blockquote>" + ARTICLE_PARAGRAPH)

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    assert "Mayor Jane Smith" in [p.text for p in paragraphs]
