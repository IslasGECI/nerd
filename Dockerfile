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
    pylint \
    pytest-cov \
    pytest \
    rope
RUN apt update && apt install --yes \
    shellcheck
RUN make install
CMD make
