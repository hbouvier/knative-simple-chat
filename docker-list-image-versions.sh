#!/bin/sh
IMAGE=${1:-spacy_fr_lemmatizer}
wget -q https://registry.hub.docker.com/v1/repositories/hbouvier/${IMAGE}/tags -O -  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'

