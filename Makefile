# Author:Mihai Criveti
# Description: Makefile for the ica_integrations_host repository
# Usage: make # this will print the help


# Project variables
PROJECT_NAME = ica_integrations_host
DOCS_DIR = docs
HANDSDOWN_PARAMS = -o $(DOCS_DIR)/ -n ica_integrations_host --name 'IBM Consulting Assistants Integrations Host' --cleanup
DIRS_TO_CLEAN := __pycache__ .pytest_cache .tox .ruff_cache .pyre .mypy_cache .pytype

# VENV
VENVS_DIR := $(HOME)/.venv
VENV_DIR := $(VENVS_DIR)/ica_integrations_host

.PHONY: help

# help: 🌐 IBM CONSULTING ASSISTANTS INTEGRATIONS HOST
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
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m pip install --upgrade pip setuptools pdm uv"
	#@python3 -m uv pip install ica_integrations_host[dev]
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
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m uv pip install '.[dev,libica_local,routes_sdv,routes_code_splitter,routes_crew_ai,routes_python_executor,routes_autogen]'"

# help: sbom                           - Create a venv, install basic dependencies, generate SBOM, and add to docs
.PHONY: sbom
sbom:
	# Create a separate virtual environment for SBOM generation
	@rm -Rf "$(VENV_DIR).sbom"
	@python3 -m venv "$(VENV_DIR).sbom"
	@/bin/bash -c "source $(VENV_DIR).sbom/bin/activate && python3 -m uv pip install --upgrade pip setuptools pdm uv && python3 -m uv pip install .[dev,libica_local,routes_sdv,routes_code_splitter,routes_autogen,routes_crew_ai]"

	# Install cyclonedx-bom and sbom2doc in the main virtual environment
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m uv pip install cyclonedx-bom sbom2doc"

	# Generate the SBOM using the sbom virtual environment path
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python -m cyclonedx_py environment --validate \"$(VENV_DIR).sbom\" --pyproject pyproject.toml --gather-license-texts > $(PROJECT_NAME).sbom.json"

	# Generate the Markdown documentation from the SBOM using the main virtual environment
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && sbom2doc -i $(PROJECT_NAME).sbom.json -f markdown -o $(DOCS_DIR)/docs/test/sbom.md"

	# Scan for vulnerabilities with trivy
	@trivy sbom $(PROJECT_NAME).sbom.json | tee -a $(DOCS_DIR)/docs/test/sbom.md
	@/bin/bash -c "source $(VENV_DIR).sbom/bin/activate && python3 -m pdm outdated | tee -a $(DOCS_DIR)/docs/test/sbom.md"


# help:
# help: 📖 DOCUMENTATION
# help: images                         - generate SVG from ica_integrations_host classes and package for documentation
.PHONY: images
images:
	@mkdir -p docs/docs/design/images
	@code2flow app/ --output docs/docs/design/images/code2flow.dot || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black docs/docs/design/images/code2flow.dot -o docs/docs/design/images/code2flow.svg || true
	@python3 -m pip install snakefood3
	@python3 -m snakefood3 app ica_integrations_host > snakefood.dot
	@dot -Tpng -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=12 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=10 -Efontcolor=black snakefood.dot -o docs/docs/design/images/snakefood.png || true
	@pyreverse --colorized app || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black packages.dot -o docs/docs/design/images/packages.svg || true
	@dot -Tsvg -Gbgcolor=transparent -Gfontname="Arial" -Nfontname="Arial" -Nfontsize=14 -Nfontcolor=black -Nfillcolor=white -Nshape=box -Nstyle="filled,rounded" -Ecolor=gray -Efontname="Arial" -Efontsize=14 -Efontcolor=black classes.dot -o docs/docs/design/images/classes.svg || true
	@rm packages.dot classes.dot snakefood.dot || true


# help: docs                           - Generate project documentation
.PHONY: docs
docs:
	$(MAKE) images
	# @rm -rf docs/docs/app; rm -rf docs/docs/coverage;
	# @coverage html -d docs/docs/coverage --include="app/*"
	@handsdown --external https://github.com/destiny/ica_integrations_host/ -o docs/docs -n app --name "ica_integrations_host" --cleanup
	@find docs/docs/app -type f -exec sed -i 's#https://github.com/destiny#https://github.ibm.com/destiny#g' {} \;
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
	@rm -rf docs/docs/app; rm -rf docs/docs/coverage;
	@coverage html -d docs/docs/coverage --include="app/*"
	@handsdown --external https://github.com/destiny/ica_integrations_host/ -o docs/docs -n app --name "ica_integrations_host" --cleanup
	@find docs/docs/app -type f -exec sed -i '' 's#https://github.com/destiny#https://github.ibm.com/destiny#g' {} \;
	@sed -i '' 's#https://github.com/destiny#https://github.ibm.com/destiny#g' docs/docs/README.md
	@cp README.md docs/docs/index.md
	@cd docs; make venv build; rm -rf ../site; mv site ../


# help:
# help: 💻 DEVELOPMENT TARGETS
# help: serve                          - run uvicorn development server
.PHONY: serve
serve:
	@uvicorn app.server:app --host 0.0.0.0 --port 8080 --reload --reload-exclude='public/'

# help: lint                           - Run linters over the project source
.PHONY: lint
lint:
	@printf '# Linting code (static analysis)\n'
	@printf '\n## Sorting imports with isort\n\n```\n'
	@isort app/ || true
	@printf '\n\n```\n\n## Linting with flake8\n\n```\n'
	@flake8 app/ || true
	@printf '\n\n```\n\n## Linting with pylint\n\n```\n'
	@pylint app/ || true
	@printf '\n\n```\n\n## Linting with mypy\n\n```\n'
	@mypy --namespace-packages -p ica_integrations_host > /dev/null || true
	@yes | mypy --install-types > /dev/null || true
	@mypy --namespace-packages -p ica_integrations_host || true
	@printf '\n\n```\n\n## Linting with bandit\n\n```\n'
	@bandit -r app/ || true
	@printf '\n\n```\n\n## Linting with pydocstyle\n\n```\n'
	@pydocstyle app/ || true
	@printf '\n\n```\n\n## Linting with pycodestyle\n\n```\n'
	@pycodestyle app/ || true
	@printf '\n\n```\n\n## Linting with pre-commit hooks\n\n```\n'
	@pre-commit run -a --color=never|| true
	@printf '\n\n```\n\n## Linting with ruff\n\n```\n'
	@ruff check app/ || true
	@ruff format app/ || true
	@printf '\n\n```\n\n'
	@printf '## Linting with pyright\n\n```\n'
	@pyright app || true
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
	radon mi -s app || true
	radon cc -s app || true
	radon hal app || true
	radon raw -s app || true
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
	pytype --keep-going app/ || true
	@printf '\n```\n\n'
	@printf "\n## Darglint\n"
	@printf '\n\n```\n'
	darglint . || true
	@printf '\n```\n\n'

# help: importchecker                  - check imports
.PHONY: importchecker
importchecker:
	@importchecker app

# help: fawltydeps                     - fawltydeps metrics. Some false positives.
.PHONY: fawltydeps
fawltydeps:
	@printf "\n## Fawltydeps\n"
	@printf '\n\n```\n'
	@fawltydeps --detailed app || true
	@printf '\n```\n\n'


# help: wily                           - wily maintainability metrics
.PHONY: wily
wily:
	@printf "\n## Wily report\n\n"
	@printf '\n\n```\n\n'
	@git stash
	@wily build -n 10 app > /dev/null || true
	@wily report app || true
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
	python3 -m cProfile -o icacli.prof app/icacli/assistants.py prompt --prompt="What is OpenShift" --model_id_or_name="Mixtral 8x7b Instruct" --refresh_data # TODO: adapt to ica_container_host
	snakeviz icacli.prof --server

# help: pstats                         - generate PNG of pstats
.PHONY: pstats
pstats:
	python3 -m cProfile -o icacli.pstats app/icacli/assistants.py prompt --prompt="What is OpenShift" --model_id_or_name="Mixtral 8x7b Instruct" --refresh_data
	gprof2dot -w -e 3 -n 3 -s -f pstats icacli.pstats  | dot -Tpng -o docs/docs/test/images/icacli-pstats.png


# help: spellcheck                     - spellcheck
.PHONY: spellcheck
spellcheck:
	pyspelling || true

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
	settings-doc generate --class ica_integrations_host.ica_settings.Settings --output-format dotenv > .ica.env.sample
	settings-doc generate --class ica_integrations_host.ica_settings.Settings --output-format markdown --heading-offset 3 > .ica.env.md

# help: build                          - Build a python wheel with pdm build
.PHONY: build
build:
	pdm build

# help: run                            - run uvicorn with ASSISTANTS_DEBUG=1 on port 8083
.PHONY: run
run:
	ASSISTANTS_DEBUG=1 SERVER_NAME="http://127.0.0.1" uvicorn app.server:app --host 0.0.0.0 --port 8083


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
	@coverage run --append --source=${PWD}/app -m doctest -v app/ica_integrations_host/ || true
	@coverage run --append --source=${PWD}/app -m doctest -v app/icacli/ || true
	@coverage report
	@coverage html -d docs/docs/coverage --include="app/*"
	@printf '\n```\n'

# help: unittest                       - run all unit tests using pytest
.PHONY: unittest
unittest:
	@printf "# Unit tests\n\n" > docs/docs/test/unittest.md
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && python3 -m pytest -p pytest_cov --reruns=1 --reruns-delay 30 --md-report --md-report-output=docs/docs/test/unittest.md --dist loadgroup -n 8 -rA --cov-append --capture=tee-sys -v --durations=120 --doctest-modules app/ --cov-report=term --cov=app --ignore=test.py tests/ || true"
	@printf \n'## Coverage report\n\n'
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && coverage report --format=markdown -m --no-skip-covered"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && coverage html -d docs/docs/coverage --include=app/*"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && coverage xml"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && coverage-badge -fo docs/docs/images/coverage.svg"

# help: pip-licenses                   - run pip-licenses to show dependency license list
.PHONY: pip-licenses
pip-licenses:
	@python3 -m uv pip install pip-licenses; pip-licenses

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
	uv pip install tox-travis tox-pdm
	pdm add -G dev
	pdm add -G libica_local
	pdm python install 3.9
	pdm python install 3.10
	pdm python install 3.11
	pdm python install 3.12
	python3 -m tox -p 2

# help:
# help: 📦 CONTAINER BUILD
# help: podman-dev                     - build the container for dev
podman-dev:
	podman build --ssh default --platform=linux/amd64 --squash --platform=linux/amd64 -t ica/ica_integrations_host-dev .

# help: podman                         - build the container
podman:
	podman build --ssh default --platform=linux/amd64 --squash -t ica/ica_integrations_host .
	podman images ica/ica_integrations_host

# help: podman-run                     - run the container
podman-run:
	podman stop ica_integrations_host || echo "stopped"
	podman rm ica_integrations_host || echo "deleted"
	podman run \
    --name ica_integrations_host \
    --env-file=.env \
    -e GUNICORN_WORKERS=3 \
    -e ICA_AUTH_TOKENS=${ICA_AUTH_TOKENS} \
    -p 8080:8080 \
    --restart=always \
    --memory=2048m \
    --cpus=1 \
    --log-opt path=/var/log/ica_integrations_host.log \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    --health-cmd="curl --fail http://localhost:8080/health || exit 1" \
    --health-interval=1m \
    --health-retries=3 \
    --health-start-period=30s \
    --health-timeout=10s \
    -d \
    localhost/ica/ica_integrations_host
#    -v $(PWD)/public:/app/public:z \
	sleep 2
	podman logs ica_integrations_host

# help: podman-stop                    - stop and  the container
podman-stop:
	podman stop ica_integrations_host
	podman rm ica_integrations_host

# help: podman-stop                    - test the container
podman-test:
	curl --request POST 'http://localhost:8080/system/wikipedia/retrievers/search/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{"search_string": "Python programming", "results_type": "full"}' || true


# help: trivy                          - run container security tests using trivy
.PHONY: trivy
trivy:
	#@trivy fs .
	@trivy --format table --severity HIGH,CRITICAL image localhost/ica/ica_integrations_host

# help:
# help: 🔨 BUILD INTEGRATIONS
# help: integration                    - Generates a new integration route
.PHONY: integration
integration:
	@python templates/app_route/route_builder.py
