import justext


def test_words_should_be_split_by_br_tag():
    paragraphs = justext.justext('abc<br/>def becoming abcdef', justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["abc def becoming abcdef"]


def test_figcaption_is_not_glued_to_the_following_text():
    html = ("<div><figure><figcaption>Photo of a cat</figcaption></figure>"
        "Actual article text.</div>")

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["Photo of a cat", "Actual article text."]


def test_max_good_distance_limits_the_neighbour_lookup():
    good = "<p>%s</p>" % ("Some very nice and long article sentence to be good. " * 4)
    html = good + "<p>tiny</p>" * 12 + good
    stoplist = justext.get_stoplist("English")

    near = justext.justext(html, stoplist, max_good_distance=100)
    far = justext.justext(html, stoplist, max_good_distance=5)

    # without the limit a single good paragraph pulls in the whole block
    assert all(not p.is_boilerplate for p in near)
    assert [p.is_boilerplate for p in far] == [False] + [True] * 12 + [False]


ARTICLE_PARAGRAPH = "<p>%s</p>" % (
    "The council voted on Tuesday to approve the new budget for the city. " * 3)


def test_nav_is_removed():
    html = ("<article><nav><h2>Contents</h2><ul><li><a href='#budget'>Budget</a>"
        "</li></ul></nav>" + ARTICLE_PARAGRAPH * 2 + "</article>")

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    # the short heading of the table of contents used to be kept as good text
    assert "Contents" not in [p.text for p in paragraphs]


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
