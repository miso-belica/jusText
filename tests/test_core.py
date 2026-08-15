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
