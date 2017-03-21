#!/usr/bin/env bash

pandoc --from=markdown --to=rst --output=README README.md

python3 setup.py register -r pypitest
python3 setup.py sdist upload -r pypitest
python3 setup.py register -r pypi
python3 setup.py sdist upload -r pypi

rm -r -f MANIFEST README dist