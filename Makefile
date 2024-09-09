all: check coverage mutants

module = nerd
codecov_token = 84e068b0-5f49-4a9e-b08a-b90e880fbc6a

define lint
	pylint \
        --disable=bad-continuation \
        --disable=missing-class-docstring \
        --disable=missing-function-docstring \
        --disable=missing-module-docstring \
        ${1}
endef

.PHONY: \
		all \
		check \
		clean \
		coverage \
		format \
		init \
		linter \
		mutants \
		setup \
		tests

check:
	black --check --line-length 100 ${module}
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${module}
	flake8 --max-line-length 100 tests
	shellcheck */*.sh
	mypy ${module}
	mypy tests

clean:
	rm --force --recursive ${module}.egg-info
	rm --force --recursive ${module}/__pycache__
	rm --force --recursive ${module}/calibration/__pycache__
	rm --force --recursive ${module}/density_functions/__pycache__
	rm --force --recursive ${module}/io/__pycache__
	rm --force --recursive ${module}/mapping/__pycache__
	rm --force --recursive outputs
	rm --force --recursive tests/__pycache__
	rm --force .mutmut-cache
	rm --force XXinput_data.csvXX
	rm --force examples/*.py
	rm --force tests/data/imported_data.csv
	rm --force tests/test_shapefile.*

coverage: setup
	pytest --cov=${module} --cov-report=xml --verbose && \
	coverage report --show-missing

format:
	black --line-length 100 ${module}
	black --line-length 100 tests

init: init_git setup tests

init_git:
	git config --global --add safe.directory /workdir
	git config --global user.name "Ciencia de Datos • GECI"
	git config --global user.email "ciencia.datos@islas.org.mx"

linter:
	$(call lint, ${module})
	$(call lint, tests)

mutants: setup
	mutmut run --paths-to-mutate ${module}

setup: clean install

install:
	pip install --editable .

tests:
	pytest --verbose

red: format
	pytest --verbose \
	&& git restore tests/*.py \
	|| (git add tests/*.py && git commit -m "🛑🧪 Fail tests")
	chmod g+w -R .

green: format
	pytest --verbose \
	&& (git add ${module}/*/*.py tests/*.py && git commit -m "✅ Pass tests") \
	|| git restore ${module}/*/*.py
	chmod g+w -R .

refactor: format
	pytest --verbose \
	&& (git add ${module}/*/*.py tests/*.py && git commit -m "♻️  Refactor") \
	|| git restore ${module}/*/*.py tests/*.py
	chmod g+w -R .
