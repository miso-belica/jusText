import justext


def test_words_should_be_split_by_br_tag():
    paragraphs = justext.justext('abc<br/>def becoming abcdef', justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["abc def becoming abcdef"]


def test_figcaption_is_not_glued_to_the_following_text():
    html = ("<div><figure><figcaption>Photo of a cat</figcaption></figure>"
        "Actual article text.</div>")

    paragraphs = justext.justext(html, justext.get_stoplist("English"))

    assert [p.text for p in paragraphs] == ["Photo of a cat", "Actual article text."]
