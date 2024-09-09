FROM python:3.8
WORKDIR /workdir
COPY . .
RUN pip install \
    autopep8 \
    black \
    black[jupyter] \
    flake8 \
    geojsoncontour \
    ipykernel \
    markdown-code-runner \
    mutmut \
    mypy \
    pandas-stubs \
    pylint \
    pytest \
    pytest-cov \
    rope \
    types-tqdm
RUN apt update && apt install --yes \
    shellcheck
RUN make install
CMD make
