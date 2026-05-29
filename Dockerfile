FROM python:3.12
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
    mutmut==2.4.* \
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
