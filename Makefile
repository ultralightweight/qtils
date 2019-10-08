# -----------------------------------------------------------------------------
# description: General Python Makefile
# author: Daniel Kovacs <mondomhogynincsen@gmail.com>
# licence: MIT <https://opensource.org/licenses/MIT>
# version: 3.3
# supported: virtualenv, pytest
# -----------------------------------------------------------------------------

SHELL=/bin/bash

# -----------------------------------------------------------------------------
# package config
# -----------------------------------------------------------------------------

PACKAGE_HOME := .
PACAKGE_SOURCES := src
PACKAGE_TEST := test
PACKAGE_ENVIRONMENT_FILE := .environment


# -----------------------------------------------------------------------------
# build config
# -----------------------------------------------------------------------------

BUILD_DIR := $(PACKAGE_HOME)/build
BUILD_DIST_DIR := $(PACKAGE_HOME)/dist
BUILD_TARGET := sdist
BUILD_ARGS := 


# -----------------------------------------------------------------------------
# python config
# -----------------------------------------------------------------------------

PYTHON_VERSION="python3"


# -----------------------------------------------------------------------------
# virtualenv config
# -----------------------------------------------------------------------------

VIRTUALENV_DIR := .virtualenv
# VIRTUALENV_HOME := $(PACKAGE_HOME)/$(VIRTUALENV_DIR)
VIRTUALENV_HOME := $(VIRTUALENV_DIR)
VIRTUALENV_ACTIVATE := $(VIRTUALENV_HOME)/bin/activate


# -----------------------------------------------------------------------
# define checkenv-start-validation
# -----------------------------------------------------------------------

define checkenv-start-validation
	@echo "checking environment...."
	@rm -f $(PACKAGE_ENVIRONMENT_FILE)
endef


# -----------------------------------------------------------------------
# define checkenv-command
# -----------------------------------------------------------------------

define checkenv-command
	@printf "checking $(1)..." && (type $(1) >> $(PACKAGE_ENVIRONMENT_FILE) 2>&1 && echo "ok") || (echo "error: $(1) not found" >> $(PACKAGE_ENVIRONMENT_FILE) && echo "NOT FOUND" && true)
endef


# -----------------------------------------------------------------------
# define checkenv-validate
# -----------------------------------------------------------------------

define checkenv-validate
	@(grep error $(PACKAGE_ENVIRONMENT_FILE) > /dev/null 2>&1 && rm -f $(PACKAGE_ENVIRONMENT_FILE) || true)
	@( [ -f $(PACKAGE_ENVIRONMENT_FILE) ] || (echo "error: invalid environment configuration.\n\nPlease install the missing packages listed above.\n" && false) )
endef


# -----------------------------------------------------------------------
# target: _recheckenv
# -----------------------------------------------------------------------

_recheckenv::
	@rm -f $(PACKAGE_ENVIRONMENT_FILE)


# -----------------------------------------------------------------------
# target: checkenv
# -----------------------------------------------------------------------

.PHONY: checkenv
checkenv:: _recheckenv $(PACKAGE_ENVIRONMENT_FILE)


# -----------------------------------------------------------------------
# target: $(PACKAGE_ENVIRONMENT_FILE)
# -----------------------------------------------------------------------

$(PACKAGE_ENVIRONMENT_FILE):: Makefile
	$(call checkenv-start-validation)
	$(call checkenv-command,git)
	$(call checkenv-command,python)
	$(call checkenv-command,pip)
	$(call checkenv-command,virtualenv)
#	# $(call checkenv-command,wget)
#	# $(call checkenv-command,docker)
	$(call checkenv-validate)
	
# -----------------------------------------------------------------------------
# clean
# -----------------------------------------------------------------------------

.PHONY:clean
clean::
	rm -rf $(PACKAGE_ENVIRONMENT_FILE) $(VIRTUALENV_HOME) $(ASSETS_HOME) activate build dist .cache .eggs .tmp *.egg-info src/*.egg-info
	find . -name "*.pyc" -exec rm -rf {} \; || true
	find . -name "__pycache__" -exec rm -rf {} \; || true


# -----------------------------------------------------------------------------
# $(VIRTUALENV_HOME)
# -----------------------------------------------------------------------------

$(VIRTUALENV_HOME):: $(PACKAGE_ENVIRONMENT_FILE) 
	virtualenv --python $(PYTHON_VERSION) $@
	ln -sf $(VIRTUALENV_ACTIVATE) activate
	touch $@


# -----------------------------------------------------------------------------
# virtualenv
# -----------------------------------------------------------------------------

.PHONY: virtualenv
virtualenv: $(VIRTUALENV_HOME)


# -----------------------------------------------------------------------------
# $(VIRTUALENV_HOME)/deps
# -----------------------------------------------------------------------------

$(VIRTUALENV_HOME)/deps:: requirements.txt $(VIRTUALENV_HOME)
	source activate && pip install -r $<
	source activate && pip install -e .
	touch $@


# -----------------------------------------------------------------------------
# $(VIRTUALENV_HOME)/deps-%
# -----------------------------------------------------------------------------

$(VIRTUALENV_HOME)/deps-%:: requirements-%.txt $(VIRTUALENV_HOME)/deps
	source activate && pip install -r $<
	touch $@

# -----------------------------------------------------------------------------
# deps
# -----------------------------------------------------------------------------

deps:: $(VIRTUALENV_HOME)/deps

# -----------------------------------------------------------------------------
# deps-build
# -----------------------------------------------------------------------------

deps-build:: $(VIRTUALENV_HOME)/deps-build

# -----------------------------------------------------------------------------
# deps-test
# -----------------------------------------------------------------------------

deps-test:: $(VIRTUALENV_HOME)/deps-test

# -----------------------------------------------------------------------------
# deps-docs
# -----------------------------------------------------------------------------

deps-docs:: $(VIRTUALENV_HOME)/deps-docs



# -----------------------------------------------------------------------
# lint
# -----------------------------------------------------------------------

lint:: deps-test
	source activate && pylint $(PACAKGE_SOURCES)/


# -----------------------------------------------------------------------
# target: test-modules
# -----------------------------------------------------------------------

.PHONY: test-modules
test-modules:: deps-test lint
	source activate && pytest $(PACAKGE_SOURCES)/


# -----------------------------------------------------------------------
# target: test-e2e
# -----------------------------------------------------------------------

.PHONY: test-e2e
test-e2e:: deps-test
	source activate && pytest test/


# -----------------------------------------------------------------------
# target: test
# -----------------------------------------------------------------------

.PHONY: test
test:: deps-test
	source activate && pylint $(PACAKGE_SOURCES)/
	source activate && pytest --cov $(PACAKGE_SOURCES)/ $(PACAKGE_SOURCES)/ $(PACKAGE_TEST)/


# -----------------------------------------------------------------------
# target: test-%
# -----------------------------------------------------------------------

test-%:: $(PACKAGE_TEST)/%_test.py deps deps-test
	source activate && pytest $<


# -----------------------------------------------------------------------------
# shell
# -----------------------------------------------------------------------------

shell: deps
	source activate && python -i shell.py


# -----------------------------------------------------------------------
# build
# -----------------------------------------------------------------------

dist:: $(SOURCES) deps deps-build
	./setup.py $(BUILD_TARGET) $(BUILD_ARGS)
	touch dist


# -----------------------------------------------------------------------
# build
# -----------------------------------------------------------------------

build:: dist


# -----------------------------------------------------------------------
# docs
# -----------------------------------------------------------------------

docs:: deps-docs
	rm -rf docs/apidoc
	source activate && sphinx-apidoc --module-first --output-dir docs/apidoc $(PACAKGE_SOURCES)/$(PACKAGE_NAME)
	source activate && sphinx-build -M html docs/ $(BUILD_DIR)/docs/


# -----------------------------------------------------------------------------
# setup
# -----------------------------------------------------------------------------

setup:: deps deps-test deps-build deps-docs



# -----------------------------------------------------------------------
# install
# -----------------------------------------------------------------------

install:: $(SOURCES)
	./setup.py install


# -----------------------------------------------------------------------------
# bump-%
# -----------------------------------------------------------------------------

bump-%:: deps-build
	rm -rf dist
	source activate && bumpversion --list --commit --tag $(subst bump-,,$@)


# -----------------------------------------------------------------------------
# release-minor
# -----------------------------------------------------------------------------

release-minor: test bump-minor build


# -----------------------------------------------------------------------------
# release-patch
# -----------------------------------------------------------------------------

release-patch: test bump-patch build


# -----------------------------------------------------------------------------
# release-major
# -----------------------------------------------------------------------------

release-major: test bump-major build


# -----------------------------------------------------------------------------
# release
# -----------------------------------------------------------------------------

release:: test build


# -----------------------------------------------------------------------------
# release
# -----------------------------------------------------------------------------

publish:: dist
	source activate && twine upload dist/*



# -----------------------------------------------------------------------
# include package specific targets (if there is any)
# -----------------------------------------------------------------------

-include package.mk

