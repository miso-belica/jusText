#!/bin/bash

for XMLFILE in wikidumps-xml/*.xml.bz2; do
    BASENAME=`basename $XMLFILE`
    FILEID=${BASENAME%%.xml.bz2}
    DEST_DIR=wikidumps-txt/$FILEID
    if [ ! -d $DEST_DIR ]; then
        echo "Creating $DEST_DIR"
        mkdir -p $DEST_DIR
        bzcat $XMLFILE | ./WikiExtractor.py -cb 10M -o $DEST_DIR
    fi
done
