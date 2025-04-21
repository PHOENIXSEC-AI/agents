#!/bin/sh
# This script reflects the latest changes of pyproject.toml
#  into both the poetry.lock file and the virtualenv.
#  by running `poetry lock` and `poetry install --sync`
# It first configures poetry to use the right python for creation of the virtual env
set -x
set -u
set -e
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "${DIR}/.." || exit

# all python packages, in topological order
. ${DIR}/projects.sh
_projects=". ${PROJECTS}"
echo "Running on following projects: ${_projects}"
for p in $_projects
do
  cd "${DIR}/../${p}" || exit
  # Try to use pyenv local python version if available, otherwise fall back to default
  if pyenv local >/dev/null 2>&1; then
    pyenv local  # Set the local Python version
    PYTHON_PATH=$(which python3)
    if [ -n "$PYTHON_PATH" ]; then
      poetry env use "$PYTHON_PATH"
    else
      poetry env use python${DEFAULT_PYTHON_VERSION}
    fi
  else
    poetry env use python${DEFAULT_PYTHON_VERSION}
  fi
  # Use Poetry 2.x commands (no --no-update flag)
  poetry lock && poetry install
done
