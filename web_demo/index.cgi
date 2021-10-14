#!/usr/bin/env python

import cgitb
cgitb.enable()

import cgi
import codecs
import os
import sys
import urllib2

import justext
import justext.core

from distutils.sysconfig import get_python_lib
STOPLISTS_DIR = os.path.join(get_python_lib(), 'justext', 'stoplists')
STOPLISTS = {'-Any_language-': None}
for filename in os.listdir(STOPLISTS_DIR):
    if not filename.endswith('.txt'):
        continue
    filepath = os.path.join(STOPLISTS_DIR, filename)
    language = filename.rsplit('.')[0]
    STOPLISTS[language] = filepath

# get form values
form = cgi.FieldStorage()
url = form.getfirst('url', '').strip()
language = form.getfirst('language', None)
no_headings = form.getfirst('no_headings', justext.core.NO_HEADINGS_DEFAULT)
length_low_str = form.getfirst('length_low', str(justext.core.LENGTH_LOW_DEFAULT))
length_high_str = form.getfirst('length_high', str(justext.core.LENGTH_HIGH_DEFAULT))
stopwords_low_str = form.getfirst('stopwords_low', str(justext.core.STOPWORDS_LOW_DEFAULT))
stopwords_high_str = form.getfirst('stopwords_high', str(justext.core.STOPWORDS_HIGH_DEFAULT))
max_link_density_str = form.getfirst('max_link_density', str(justext.core.MAX_LINK_DENSITY_DEFAULT))
max_good_distance_str = form.getfirst('max_good_distance', str(justext.core.MAX_GOOD_DISTANCE_DEFAULT))
max_heading_distance_str = form.getfirst('max_heading_distance', str(justext.core.MAX_HEADING_DISTANCE_DEFAULT))

class FormInputError(Exception):
    pass

try:
    # parse form values
    input_errors = []
    try:
        length_low = int(length_low_str)
    except ValueError:
        input_errors.append("Length low: integer value required")
    try:
        length_high = int(length_high_str)
    except ValueError:
        input_errors.append("Length high: integer value required")
    try:
        stopwords_low = float(stopwords_low_str)
    except ValueError:
        input_errors.append("Stopwords low: float value required")
    try:
        stopwords_high = float(stopwords_high_str)
    except ValueError:
        input_errors.append("Stopwords high: float value required")
    try:
        max_link_density = float(max_link_density_str)
    except ValueError:
        input_errors.append("Max link density: float value required")
    try:
        max_good_distance = int(max_good_distance_str)
    except ValueError:
        input_errors.append("Max good distance: integer value required")
    try:
        max_heading_distance = int(max_heading_distance_str)
    except ValueError:
        input_errors.append("Max heading distance: integer value required")

    sl_options = []
    for stoplist in sorted(STOPLISTS.keys()):
        if stoplist == language:
            selected = 'selected="selected"'
        else:
            selected = ''
        sl_options.append('<option value="%s" %s>%s</option>' % (
            stoplist, selected, stoplist.replace('_', ' ')))
    select_language_options = '\n'.join(sl_options)

    if no_headings:
        no_headings_checked = 'checked="checked"'
    else:
        no_headings_checked = ''

    if input_errors:
        raise FormInputError('</br>\n'.join(input_errors))

    # process the URL, prepare for output
    processed_page = []
    if url:
        try:
            html_text = urllib2.urlopen(url).read()
        except (ValueError, urllib2.URLError, urllib2.HTTPError), e:
            raise FormInputError("Unable to retrieve the URL: %s" % str(e))

        if not STOPLISTS.get(language):
            stoplist = set()
            stopwords_low=0
            stopwords_high=0
        else:
            stoplist = set([line.strip() for line in 
                codecs.open(STOPLISTS[language], 'r', 'utf-8')])
        paragraphs = justext.justext(html_text, stoplist, length_low, length_high,
                stopwords_low, stopwords_high, max_link_density, max_good_distance,
                max_heading_distance, no_headings, enc_errors='ignore')

        for i, paragraph in enumerate(paragraphs):
            word_sequence = []
            for word in paragraph['text'].strip().split():
                encoded_word = justext.core.html_escape(word.encode('utf-8'))
                if word in stoplist:
                    word_sequence.append('<span class="stopword">%s</span>' % encoded_word)
                else:
                    word_sequence.append(encoded_word)
            text = " ".join(word_sequence)
            if paragraph['class'] == 'good':
                if paragraph['heading']:
                    class_ = 'heading'
                else:
                    class_ = 'good'
            else:
                class_ = 'bad'
            processed_page.append('<div id="pd%i" class="paragraph_details %s">' % (i, class_))
            processed_page.append('<table>')
            processed_page.append('<tr class="odd"><td class="attr">final class</td><td class="value">%s</td></tr>' % paragraph['class'])
            processed_page.append('<tr class="even"><td class="attr">cotext-free class</td><td class="value">%s</td></tr>' % paragraph['cfclass'])
            processed_page.append('<tr class="odd"><td class="attr">heading</td><td class="value">%s</td></tr>' % paragraph['heading'])
            processed_page.append('<tr class="even"><td class="attr">length (in characters)</td><td class="value">%i</td></tr>' % len(paragraph['text']))
            processed_page.append('<tr class="odd"><td class="attr">number of characters within links</td><td class="value">%i</td></tr>' % paragraph['linked_char_count'])
            processed_page.append('<tr class="even"><td class="attr">link density</td><td class="value">%.3f</td></tr>' % paragraph['link_density'])
            processed_page.append('<tr class="odd"><td class="attr">number of words</td><td class="value">%i</td></tr>' % paragraph['word_count'])
            processed_page.append('<tr class="even"><td class="attr">number of stopwords</td><td class="value">%i</td></tr>' % paragraph['stopword_count'])
            processed_page.append('<tr class="odd"><td class="attr">stopword density</td><td class="value">%.3f</td></tr>' % paragraph['stopword_density'])
            processed_page.append('<tr class="even"><td colspan="2" class="value">%s</td></tr>' % paragraph['dom_path'])
            processed_page.append('</table>')
            processed_page.append('</div>')
            processed_page.append('<p class="%s" onmouseover="show_paragraph_details(this, \'pd%i\');" onmouseout="hide_paragraph_details(this, \'pd%i\');">%s</p>' % (
                    class_, i, i, text))
except FormInputError, e:
    error = '<div id="error">%s</div>' % str(e)
else:
    error = ''


# header + input form
print "Content-type: text/html"
print
print """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript" src="script.js"></script>
<title>jusText demo</title>
</head>
<body>
<h1>jusText demo</h1>
<div class="description">
jusText is a heuristic based boilerplate removal tool.
See the project page at <a href="http://corpus.tools/wiki/Justext">Corpus tools</a>.
</div>
<form action="." method="get">
<fieldset>
%(error)s
<div id="basic_options">
<table>
  <tr>
    <td class="label">URL</td>
    <td><input name="url" type="text" value="%(url)s" class="wide" /></td>
  </tr>
  <tr>
    <td class="label">Language</td>
    <td><select name="language" />%(select_language_options)s</select></td>
  </tr>
</table>
</div>
<div id="advanced_options">
<hr/>
<table>
  <tr>
    <td>No headings</td>
    <td><input type="checkbox" name="no_headings" %(no_headings_checked)s /></td>
  </tr>
  <tr>
    <td>Length low</td>
    <td><input name="length_low" type="text" value="%(length_low_str)s" /></td>
  </tr>
  <tr>
    <td>Length high</td>
    <td><input name="length_high" type="text" value="%(length_high_str)s" /></td>
  </tr>
  <tr>
    <td>Stopwords low</td>
    <td><input name="stopwords_low" type="text" value="%(stopwords_low_str)s" /></td>
  </tr>
  <tr>
    <td>Stopwords high</td>
    <td><input name="stopwords_high" type="text" value="%(stopwords_high_str)s" /></td>
  </tr>
  <tr>
    <td>Max link density</td>
    <td><input name="max_link_density" type="text" value="%(max_link_density_str)s" /></td>
  </tr>
  <tr>
    <td>Max good paragraph distance</td>
    <td><input name="max_good_distance" type="text" value="%(max_good_distance_str)s" /></td>
  </tr>
  <tr>
    <td>Max heading distance</td>
    <td><input name="max_heading_distance" type="text" value="%(max_heading_distance_str)s" /></td>
  </tr>
</table>
</div>
<hr/>
<div>
  <input id="submit" type="submit" />
  <a href="javascript:show_advanced();" id="show_advanced_link">Show advanced options</a>
  <a href="javascript:hide_advanced();" id="hide_advanced_link" style="display: none">Hide advanced options</a>
</div>
</fieldset>
</form>
""" % {
        'error': error,
        'url': url,
        'select_language_options': select_language_options,
        'no_headings_checked': no_headings_checked,
        'length_low_str': length_low_str,
        'length_high_str': length_high_str,
        'stopwords_low_str': stopwords_low_str,
        'stopwords_high_str': stopwords_high_str,
        'max_link_density_str': max_link_density_str,
        'max_good_distance_str': max_good_distance_str,
        'max_heading_distance_str': max_heading_distance_str,
}

# output or processing
if url and not error:
    print """
<p>
  <a href="javascript:hide_boilerplate();" id="hide_boilerplate_link">Hide boilerplate</a>
  <a href="javascript:show_boilerplate();" id="show_boilerplate_link" style="display: none">Show boilerplate</a>
</p>
<div id="output_wrapper">
%s
</div>
""" % "\n".join(processed_page)

# footer
print """<div id="footer">
<hr/>
(c) Jan Pomikalek &lt;<a href="mailto:xpomikal@fi.muni.cz">xpomikal@fi.muni.cz</a>&gt;,
<a href="http://nlp.fi.muni.cz/en">NLPlab</a>, FI MU
</div>
</body>
</html>"""
