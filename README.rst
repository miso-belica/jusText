.. _jusText: http://code.google.com/p/justext/
.. _Python: http://www.python.org/
.. _lxml: http://lxml.de/

jusText
=======
Program jusText is a tool for removing boilerplate content, such as navigation
links, headers, and footers from HTML pages. It is designed to preserve mainly
text containing full sentences and it is therefore well suited for creating
linguistic resources such as Web corpora. You can
`try it online <http://nlp.fi.muni.cz/projects/justext/>`_.

This is the a fork of original code of jusText_ hosted on Google code.
Below are some "forks" that I found on GitHub:

- https://github.com/andreypopp/extracty/tree/master/justext
- https://github.com/dreamindustries/jaws/tree/master/justext
- https://github.com/says/justext
- https://github.com/chbrown/justext
- https://github.com/says/justext-app

Installation
------------
1. Make sure you have Python_ installed.
2. Download the sources::

     $ wget https://github.com/miso-belica/jusText/archive/master.zip

3. Extract the downloaded file::

     $ unzip master.zip

4. Install the package (you may need sudo or a root shell for the latter
   command)::

     $ cd jusText-master/
     $ python setup.py install

Or simply::

  pip install git+git@github.com:miso-belica/jusText.git

Dependencies
-----------
::

  lxml>=2.2.4

Usage
-----
.. code-block:: bash

  $ python -m justext -s Czech --url=http://www.zdrojak.cz/clanky/automaticke-zabezpeceni/ > text.txt
  $ python -m justext -s English english_page.html > plain_text.txt
  $ python -m justext --help # for more info

Python API
----------
.. code-block:: python

  import requests
  import justext

  response = requests.get("http://planet.python.org/")
  paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
  for paragraph in paragraphs:
    if paragraph.class_type == "good":
      print paragraph.text

Testing
-------
Run tests via

.. code-block:: bash

  $ cd tests
  $ python -tt -Wall -B -3 -m unittest discover

Acknowledgements
----------------
.. _`Natural Language Processing Centre`: http://nlp.fi.muni.cz/en/nlpc
.. _`Masaryk University in Brno`: http://nlp.fi.muni.cz/en
.. _PRESEMT: http://presemt.eu/
.. _`Lexical Computing Ltd.`: http://lexicalcomputing.com/
.. _`PhD research`: http://is.muni.cz/th/45523/fi_d/phdthesis.pdf

This software is developed at the `Natural Language Processing Centre`_ of
`Masaryk University in Brno`_ with a financial support from PRESEMT_ and
`Lexical Computing Ltd.`_ It also relates to `PhD research`_ of Jan Pomikálek.
