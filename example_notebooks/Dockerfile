FROM jupyter/minimal-notebook
USER root
WORKDIR /workdir
COPY . /workdir
COPY tests/data /workdir/tests/data
RUN apt update && apt install --yes \
    make
RUN pip install \
    black[jupyter] \
    flake8 \
    git+https://github.com/IslasGECI/nerd.git \
    matplotlib \
    nbmerge \
    pandas
CMD ["bash", "-c", "umask 000 && jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=''"]
