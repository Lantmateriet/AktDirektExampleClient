#!/bin/sh

# Test reStructuredText to html conversion.
# You need to have done: pipenv install --dev

mkdir -p build/doc/

echo Writing html to ./build/doc/

for rst in *.rst; do
  echo $rst
  pipenv run rst2html5.py  $rst build/doc/$rst.html
done
