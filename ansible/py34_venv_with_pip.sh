#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Creates a Python 3.4 virtual environment with a functional pip on
# Ubuntu 14.04.  The underlying bug and solution is described at
# https://gist.github.com/denilsonsa/21e50a357f2d4920091e

VENVDIR=$1
pyvenv-3.4 --without-pip "${VENVDIR}"
set +u
source "${VENVDIR}/bin/activate"
set -u
curl https://bootstrap.pypa.io/get-pip.py | python
