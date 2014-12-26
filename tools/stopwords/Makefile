wikidumps_txt=$(wildcard wikidumps-txt/*wiki-*-pages-articles)
lang_codes=$(foreach wikidump,$(wikidumps_txt),$(shell echo $(wikidump) | sed 's,^wikidumps-txt/\([a-z][a-z_]*\)wiki-.*,\1,'))
freqlists=$(addprefix freqlists/,$(addsuffix -freqlist.txt.gz,$(lang_codes)))
stoplists=$(addprefix stoplists/,$(addsuffix -stoplist.txt,$(lang_codes)))
wikidumps_txt_samples=$(addprefix wikidumps-txt-samples/,$(addsuffix -sample.txt,$(lang_codes)))

all: $(freqlists) $(stoplists) $(wikidumps_txt_samples)

wikidumps-xml: wiki-lang_codes-10k_art_plus.csv
	mkdir -p $@
	cd $@ && \
	for CODE in `cat ../$< | tr - _`; do \
		if [ ! -f $${CODE}wiki-*-pages-articles.xml.bz2 ]; then \
			wget -O /tmp/wp-index.html http://dumps.wikimedia.org/$${CODE}wiki/; \
			LAST_DUMP_DATE=`grep -B1 latest/ < /tmp/wp-index.html | head -n1 | grep -o '[0-9]\{8\}' | head -n1`; \
			wget http://dumps.wikimedia.org/$${CODE}wiki/$$LAST_DUMP_DATE/$${CODE}wiki-$$LAST_DUMP_DATE-pages-articles.xml.bz2; \
			rm -f /tmp/wp-index.html; \
		fi; \
	done

wikidumps-txt: wikidumps-xml
	./xml2txt-all.sh

wikidumps-txt-samples/%-sample.txt: wikidumps-txt/%wiki-*-pages-articles/
	bzcat $</*/wiki*.bz2 | grep -v '^<doc ' | sed 's,<[^>]*>,,g' | head -c1000000 >$@

freqlists/%-freqlist.txt.gz: wikidumps-txt/%wiki-*-pages-articles/
	bzcat $</*/wiki*.bz2 | grep -v '^<doc ' | sed 's,<[^>]*>,,g' | ./text2freqlist.py | gzip > $@

stoplists/%-stoplist.txt: freqlists/%-freqlist.txt.gz
	zcat $< | ./freqlist2stoplist.py > $@

rename: wiki-lang_codes.csv
	mkdir -p stoplists-renamed
	for CODE in $(lang_codes); do \
		LANG=`grep "^$$CODE," <$< | cut -d, -f2`; \
        echo cp stoplists/$${CODE}-stoplist.txt stoplists-renamed/$${LANG}.txt; \
        cp stoplists/$${CODE}-stoplist.txt stoplists-renamed/$${LANG}.txt; \
	done
