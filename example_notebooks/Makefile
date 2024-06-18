all: check_notebook format_notebook

.PHONY: \
		all \
		check_notebook \
		format_notebook

check_notebook:
	black --check --line-length 100 /workdir/*.ipynb

format_notebook:
	black --line-length 100 /workdir/*.ipynb
