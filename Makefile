.PHONY: install-dev
install-dev:	## install project including all development dependencies
	pip install -e .[test,dev,docs]

.PHONY: maintainability
maintainability:  ## run maintainability checks
	@radon cc --total-average -nB -s src

.PHONY: vulnerabilities audit
vulnerabilities:  ## run vulnerability checks
audit:
	@pip-audit

.PHONY: test coverage coverage-ci
test:  ## run unit tests
	@pytest
coverage:	## collect coverage data and open report in browser
	pwd
	find . -type d
	ls -latR ./tests
	@pytest --doctest-modules --cov --cov-config=pyproject.toml --cov-branch --cov-report term-missing --cov-report html:build/coverage --cache-clear -vvvv
	@test -z "$(CI)" \
		&& ( echo "Opening 'build/coverage/index.html'..."; open build/coverage/index.html || start build/coverage/index.html )\
		|| echo ""
coverage-ci:
	@CI=true "$(MAKE)" coverage

.PHONY: compatibility tox
compatibility:	## run a Python version compatibility test
tox:
	@tox

.PHONY: lint
lint:	## run static code checks
	@ruff check src tests

.PHONY: format format-ci
format:	## run static code formatting
	@ruff format src tests
format-ci:
	@ruff format --check --diff src tests

.PHONY: docs docs-clean docs-live docs-open
DOCS_TARGET?=build/docs
docs:	## build documentation
	cd docs && BUILDDIR=../${DOCS_TARGET} "$(MAKE)" -b html

docs-clean:	## clears the docs directory and rebuilds
	rm -rf ${DOCS_TARGET}
	"$(MAKE)" docs

docs-live:	## serve documentation
	cd docs && "$(MAKE)" serve

docs-open:	## open documentation
	(open build/docs/html/index.html || start build/docs/html/index.html) || echo ""


.PHONY: help
# a nice way to document Makefiles, found here: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
