.. _jusText: http://code.google.com/p/justext/
.. _Python: http://www.python.org/
.. _lxml: http://lxml.de/

jusText
=======
.. image:: https://api.travis-ci.org/miso-belica/jusText.png?branch=master
  :target: https://travis-ci.org/miso-belica/jusText

Program jusText is a tool for removing boilerplate content, such as navigation
links, headers, and footers from HTML pages. It is
`designed <doc/algorithm.rst>`_ to preserve
mainly text containing full sentences and it is therefore well suited for
creating linguistic resources such as Web corpora. You can
`try it online <http://nlp.fi.muni.cz/projects/justext/>`_.

This is a fork of original (currently unmaintained) code of jusText_ hosted
on Google Code. Below are some alternatives that I found:

- http://code.google.com/p/boilerpipe/
- http://sourceforge.net/projects/webascorpus/?source=navbar
- https://github.com/jiminoc/goose
- https://github.com/grangier/python-goose
- https://github.com/miso-belica/readability.py
- https://github.com/dcramer/decruft
- https://github.com/FeiSun/ContentExtraction

- https://github.com/JalfResi/justext
- https://github.com/andreypopp/extracty/tree/master/justext
- https://github.com/dreamindustries/jaws/tree/master/justext
- https://github.com/says/justext
- https://github.com/chbrown/justext
- https://github.com/says/justext-app


Installation
------------
Make sure you have Python_ 2.6+/3.2+ and `pip <https://crate.io/packages/pip/>`_
(`Windows <http://docs.python-guide.org/en/latest/starting/install/win/>`_,
`Linux <http://docs.python-guide.org/en/latest/starting/install/linux/>`_) installed.
Run simply (preferred way):

.. code-block:: bash

  $ [sudo] pip install justext


Or for the fresh version:

.. code-block:: bash

  $ [sudo] pip install git+git://github.com/miso-belica/jusText.git


Or if you have to:

.. code-block:: bash

  $ wget https://github.com/miso-belica/jusText/archive/master.zip # download the sources
  $ unzip master.zip # extract the downloaded file
  $ jusText-master/
  $ [sudo] python setup.py install # install the package


Dependencies
------------
::

  lxml>=2.2.4


Usage
-----
.. code-block:: bash

  $ python -m justext -s Czech -o text.txt http://www.zdrojak.cz/clanky/automaticke-zabezpeceni/
  $ python -m justext -s English -o plain_text.txt english_page.html
  $ python -m justext --help # for more info


Python API
----------
.. code-block:: python

  import requests
  import justext

  response = requests.get("http://planet.python.org/")
  paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
  for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
      print paragraph.text


Testing
-------
Run tests via

.. code-block:: bash

  $ nosetests-2.6 && nosetests-3.2 && nosetests-2.7 && nosetests-3.3


Acknowledgements
----------------
.. _`Natural Language Processing Centre`: http://nlp.fi.muni.cz/en/nlpc
.. _`Masaryk University in Brno`: http://nlp.fi.muni.cz/en
.. _PRESEMT: http://presemt.eu/
.. _`Lexical Computing Ltd.`: http://lexicalcomputing.com/
.. _`PhD research`: http://is.muni.cz/th/45523/fi_d/phdthesis.pdf

This software has been developed at the `Natural Language Processing Centre`_ of
`Masaryk University in Brno`_ with a financial support from PRESEMT_ and
`Lexical Computing Ltd.`_ It also relates to `PhD research`_ of Jan Pomikálek.
