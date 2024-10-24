# Author:Mihai Criveti
# Description: Makefile for the libica Python library
# Usage: make # this will print the help


# Project variables
PROJECT_NAME = libica
DOCS_DIR = docs
HANDSDOWN_PARAMS = -o $(DOCS_DIR)/ -n ICAClient --name 'Assistants API Client' --cleanup
DIRS_TO_CLEAN := __pycache__ .pytest_cache .tox .ruff_cache .pyre .mypy_cache .pytype

# VENV
VENVS_DIR := $(HOME)/.venv
VENV_DIR := $(VENVS_DIR)/consulting_assistants_api

.PHONY: help

# help: IBM CONSULTING ASSISTANTS INTEGRATIONS AND EXTENSIONS SDK 🤖🔧
# help: https://pages.github.ibm.com/destiny/consulting_assistants_api/
#
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help:
# help: 🔧 INSTALLATION
# help: venv                           - create a clean virtual environment for development
.PHONY: venv
venv:
	@rm -Rf "$(VENV_DIR)"
	@test -d "$(VENVS_DIR)" || mkdir -p "$(VENVS_DIR)"
	@python3 -m venv "$(VENV_DIR)"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m pip install --upgrade pip pdm"
	#@python3 -m pip install libica[dev]
	@echo -e "Enter virtual environment using:\n. $(VENV_DIR)/bin/activate\n"

# help: activate                       - enter existing venv
.PHONY: activate
activate:
	@echo -e "Enter virtual environment using:\n. $(VENV_DIR)/bin/activate\n"
	@. $(VENV_DIR)/bin/activate
	@echo "export MYPY_CACHE_DIR=/tmp/cache/mypy/$(PROJECT_NAME)"
	@echo "export PYTHONPYCACHEPREFIX=/tmp/cache/$(PROJECT_NAME)"

# help: install                        - Install project dependencies, including development dependencies
.PHONY: install
install:
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m pip install '.[dev,langchain]' && python3 -m pdm lock && python3 -m pdm sync"

# help:
# help: 📖 DOCUMENTATION
# help: images                         - generate SVG from libica classes and package for documentation
.PHONY: images
images:
	@mkdir -p docs/docs/design/images
	@code2flow src/ --output docs/docs/design/images/code2flow.dot || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black docs/docs/design/images/code2flow.dot -o docs/docs/design/images/code2flow.svg || true
	@python3 -m pip install snakefood3
	@python3 -m snakefood3 src libica > snakefood.dot
	@dot -Tpng -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=12 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=10 -Efontcolor=black snakefood.dot -o docs/docs/design/images/snakefood.png || true
	@pyreverse --colorized src || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black packages.dot -o docs/docs/design/images/packages.svg || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black classes.dot -o docs/docs/design/images/classes.svg || true
	@rm packages.dot classes.dot snakefood.dot || true


# help: docs                           - Generate project documentation
.PHONY: docs
docs:
	$(MAKE) images
	@cp -r images/demo/ docs/docs/images/
	@rm -rf docs/docs/src; rm -rf docs/docs/coverage;
	@coverage html -d docs/docs/coverage --include="src/*"
	@handsdown --external https://github.com/destiny/consulting_assistants_api/ -o docs/docs -n src --name "libica and icacli" --cleanup
	@find docs/docs/src -type f -exec sed -i 's#https://github.com/destiny#https://github.ibm.com/destiny#g' {} \;
	@sed -i 's#https://github.com/destiny#https://github.ibm.com/destiny#g' docs/docs/README.md
	@cp README.md docs/docs/index.md
	@cd docs; make venv build; rm -rf ../site; mv site ../

# help: pytest-examples                - test documentation using pytest-examples
.PHONY: pytest-examples
pytest-examples:
	pytest -v test_readme.py

# help: docs-mac                       - sed is broken on Mac, use workaround
.PHONY: docs-mac
docs-mac:
	$(MAKE) images
	@rm -rf docs/docs/src; rm -rf docs/docs/coverage;
	@coverage html -d docs/docs/coverage --include="src/*"
	@handsdown --external https://github.com/destiny/consulting_assistants_api/ -o docs/docs -n src --name "libica and icacli" --cleanup
	@find docs/docs/src -type f -exec sed -i '' 's#https://github.com/destiny#https://github.ibm.com/destiny#g' {} \;
	@sed -i '' 's#https://github.com/destiny#https://github.ibm.com/destiny#g' docs/docs/README.md
	@cp README.md docs/docs/index.md
	@cd docs; make venv build; rm -rf ../site; mv site ../


# help: manpage                        - generate and install manpage
.PHONY: manpage
manpage:
	@argparse-manpage \
		--output icacli.1 --pyfile src/icacli/assistants.py \
		--author "Mihai Criveti" --author-email "crmihai1@ie.ibm.com" \
		--description "IBM Consulting Assistants Extensions API - CLI" \
		--prog icacli \
		--manual-title icacli \
		--function=setup_parser \
		--project-name icacli --url "https://github.ibm.com/destiny/consulting_assistants_api"
	@./tools/install-manpage.py


# help:
# help: 💻 DEVELOPMENT TARGETS
# help: lint                           - Run linters over the project source
.PHONY: lint
lint:
	@printf '# Linting code (static analysis)\n'
	@printf '\n## Sorting imports with isort\n\n```\n'
	@isort src/ || true
	@printf '\n\n```\n\n## Linting with flake8\n\n```\n'
	@flake8 src/ || true
	@printf '\n\n```\n\n## Linting with pylint\n\n```\n'
	@pylint src/ || true
	@printf '\n\n```\n\n## Linting with mypy\n\n```\n'
	@mypy --namespace-packages -p libica -p icacli > /dev/null || true
	@yes | mypy --install-types > /dev/null || true
	@mypy --namespace-packages -p libica -p icacli|| true
	@printf '\n\n```\n\n## Linting with bandit\n\n```\n'
	@bandit -r src/ || true
	@printf '\n\n```\n\n## Linting with pydocstyle\n\n```\n'
	@pydocstyle src/ || true
	@printf '\n\n```\n\n## Linting with pycodestyle\n\n```\n'
	@pycodestyle src/ || true
	@printf '\n\n```\n\n## Linting with pre-commit hooks\n\n```\n'
	@pre-commit run -a --color=never|| true
	@printf '\n\n```\n\n## Linting with ruff\n\n```\n'
	@ruff check src/ || true
	@ruff format src/ || true
	@printf '\n\n```\n\n'
	@printf '## Linting with pyright\n\n```\n'
	@pyright src/libica src/icacli || true
	@printf '\n\n```\n\n'
	@printf "## Outdated packages / installed packages:"
	@printf '\n\n```\n\n'
	@echo "pdm outdated:"
	@pdm outdated
	@echo "pdm list --include default"
	@pdm list --include default
	@pdm list --include default --graph
	@printf '\n\n```\n\n'
	@printf "## Licenses\n\n"
	@pip-licenses -f markdown -u -p $$(pdm list --include default --fields=name --csv | awk 'NR > 1 {print}' | xargs)
	@printf "\n## Radon maintainability metrics\n"
	@printf '\n\n```\n'
	radon mi -s src || true
	radon cc -s src || true
	radon hal src || true
	radon raw -s src || true
	@printf '\n```\n\n'
	@printf "\n## Pyroma package checker\n"
	@printf '\n\n```\n'
	@pyroma -d .
	@printf '\n```\n\n'
	@printf "\n## Pyre check\n"
	@printf '\n\n```\n'
	@pyre || true
	@printf '\n```\n\n'
	@printf "\n## Spellcheck\n"
	@printf '\n\n```\n'
	@$(MAKE) spellcheck
	@printf '\n```\n\n'
	@printf "\n## Importchecker\n"
	@printf '\n\n```\n'
	@$(MAKE) importchecker
	@printf '\n```\n\n'
	@printf "\n## Pytype\n"
	@printf '\n\n```\n'
	pytype --keep-going src/libica || true
	pytype --keep-going src/icacli || true
	@printf '\n```\n\n'

# help: importchecker                  - check imports
.PHONY: importchecker
importchecker:
	@importchecker src

# help: fawltydeps                     - fawltydeps metrics. Some false positives.
.PHONY: fawltydeps
fawltydeps:
	@printf "\n## Fawltydeps\n"
	@printf '\n\n```\n'
	@fawltydeps --detailed src || true
	@printf '\n```\n\n'


# help: wily                           - wily maintainability metrics
.PHONY: wily
wily:
	@printf "\n## Wily report\n\n"
	@printf '\n\n```\n\n'
	@git stash
	@wily build -n 10 src > /dev/null || true
	@wily report src || true
	@git stash pop
	@printf '\n```\n\n'

# help: pyre                           - run pyre static analyzer
.PHONY: pyre
pyre:
	@pyre

# help: depend                         - Output requirements in requirements.txt format
.PHONY: depend
depend:
	pdm list --freeze
	#python3 -m pip list --format=freeze > requirements.pipfreeze

# help: snakeviz                       - run `icacli prompt` with cProfile, and open snakeviz to visualize results
.PHONY: snakeviz
snakeviz:
	python3 -m cProfile -o icacli.prof src/icacli/assistants.py prompt --prompt="What is OpenShift" --model_id_or_name="Mixtral 8x7b Instruct" --refresh_data
	snakeviz icacli.prof --server

# help: pstats                         - generate PNG of pstats
.PHONY: pstats
pstats:
	python3 -m cProfile -o icacli.pstats src/icacli/assistants.py prompt --prompt="What is OpenShift" --model_id_or_name="Mixtral 8x7b Instruct" --refresh_data
	gprof2dot -w -e 3 -n 3 -s -f pstats icacli.pstats  | dot -Tpng -o docs/docs/test/images/icacli-pstats.png


# help: spellcheck                     - spellcheck
.PHONY: spellcheck
spellcheck:
	pyspelling

# help: spellcheck-sort                - sort words in .spellcheck-en.txt
.PHONY: spellcheck-sort
spellcheck-sort: .spellcheck-en.txt
	sort -d -f -o $< $<


# help: clean                          - Clean up the project (remove compiled files, documentation, etc.)
.PHONY: clean
clean:
	@echo "#### Cleaning up... ####"
	for dir in $(DIRS_TO_CLEAN); do \
		find . -type d -name "$$dir" -exec rm -rf {} +; \
	done
	rm -rf site/
	rm -rf dist/
	rm -f .coverage
	rm -f coverage.xml
	rm -f docs/docs/test/{unittest,full,index,test}.md
	rm -rf docs/docs/coverage
	@echo "#### Cleanup complete. ####"

# help: settings-doc                   - Generate settings documentation and sample dotenv file
.PHONY: settings-doc
settings-doc:
	settings-doc generate --class libica.ica_settings.Settings --output-format dotenv > .ica.env.sample
	settings-doc generate --class libica.ica_settings.Settings --output-format markdown --heading-offset 3 > .ica.env.md

# help: build                          - Build a python wheel with pdm build
.PHONY: build
build:
	pdm build

# help:
# help: 🧪 TEST COVERAGE
# help: test                           - Run tests for the project
.PHONY: test
test:
	@python3 ./test.py --commands-file test/test_cover.sh --output-file docs/docs/test/test.md --output-file-full docs/docs/test/full.md --summary-file docs/docs/test/index.md --max-output-lines 10

# help: doctest                        - Run doctest for the project
.PHONY: doctest
doctest:
	@printf '# Doctest results\n\n```\n'
	@coverage run --append --source=${PWD}/src -m doctest -v src/libica/ || true
	@coverage run --append --source=${PWD}/src -m doctest -v src/icacli/ || true
	@coverage report
	@coverage html -d docs/docs/coverage --include="src/*"
	@printf '\n```\n'

# help: coverage                       - perform test coverage checks
.PHONY: coverage
coverage:
	@python3 ./test.py --commands-file test/test_cover.sh --output-file docs/docs/test/test.md --output-file-full docs/docs/test/full.md --summary-file docs/docs/test/index.md --max-output-lines 10
	@coverage report --format=markdown -m --no-skip-covered
	@echo "" >> docs/docs/test/index.md
	@coverage report --format=markdown -m --no-skip-covered >> docs/docs/test/index.md
	@coverage html -d docs/docs/coverage --include="src/*"
	@coverage xml
	@coverage-badge -fo docs/docs/images/coverage.svg && cp images/coverage.svg docs/docs/images/coverage.svg


# help: unittest                       - run all unit tests using pytest
.PHONY: unittest
unittest:
#	@python3 -m pytest -n auto -rA --cov-append --capture=tee-sys -v --durations=100 --doctest-modules src/libica src/icacli --cov-report=term --cov=src/libica --cov=src/icacli --ignore=test.py tests/
	@printf "# Unit tests\n\n" > docs/docs/test/unittest.md
	@python3 -m pytest -p pytest_cov --reruns=3 --reruns-delay 30 --md-report --md-report-output=docs/docs/test/unittest.md --dist loadgroup -n 8 -rA --cov-append --capture=tee-sys -v --durations=100 --doctest-modules src/libica src/icacli --cov-report=term --cov=src/libica --cov=src/icacli --ignore=test.py tests/ || true
	@printf \n'## Coverage report\n\n'
	@coverage report --format=markdown -m --no-skip-covered
	@coverage html -d docs/docs/coverage --include="src/*"
	@coverage xml
	@coverage-badge -fo docs/docs/images/coverage.svg && cp images/coverage.svg docs/docs/images/coverage.svg

# help: pip-licenses                   - run pip-licenses to show dependency license list
.PHONY: pip-licenses
pip-licenses:
	@python3 -m pip install pip-licenses; pip-licenses

# help: scc                            - run code quality metrics, mccabe, lines of code (needs scc)
.PHONY: scc
scc:
	@scc --by-file -i py,sh .

# help: install-scc-linux              - Install scc on linux in /tmp
.PHONY: install-scc-linux
install-scc-linux:
	wget https://github.com/boyter/scc/releases/download/v3.2.0/scc_Linux_x86_64.tar.gz -O /tmp/scc_Linux_x86_64.tar.gz
	tar zxf /tmp/scc_Linux_x86_64.tar.gz -C /tmp
	/tmp/scc --version

# help: scc-report                     - generate scc report for build using /tmp/scc
.PHONY: scc-report
scc-report:
	@printf "# Lines of Code Report\n\n"
	@/tmp/scc . --format=html-table
	@printf "\n\n## Files report\n\n"
	@/tmp/scc -i py,sh,yaml,,toml,md --by-file . --format=html-table

# help: tox                            - run tox build, testing across multiple python versions
.PHONY: tox
tox:
	pip install tox-travis tox-pdm
	pdm add -G dev
	pdm add -G langchain
	pdm python install 3.9
	pdm python install 3.10
	pdm python install 3.11
	pdm python install 3.12
	python3 -m tox -p 2

# help:
# help: 📦 CONTAINER BUILD
# help: podman                         - build the container
podman:
	podman build --squash -t ica/icacli .

# help: podman-run                     - run the container
podman-run:
	podman run --env-file ~/.config/icacli/.ica.env -e ASSISTANTS_CONFIG_FILE_LOCATION=/tmp/.ica.env localhost/ica/icacli icacli get-models --refresh_data


# help: trivy                          - run container security tests using trivy
.PHONY: trivy
trivy:
	#@trivy fs .
	@trivy --format table --severity HIGH,CRITICAL image localhost/ica/icacli
	@trivy fs .
