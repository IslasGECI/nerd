<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
[![status](https://joss.theoj.org/papers/f68799e8216e0ed1c1d06feb095e6994/status.svg)](https://joss.theoj.org/papers/f68799e8216e0ed1c1d06feb095e6994)
# NERD: Numerical Estimation of Rodenticide Density

The eradication of rodents is central to island restoration efforts and the aerial broadcast of
rodenticide bait is the preferred dispersal method.
To improve accuracy and expedite the evaluation of aerial operations, we developed an algorithm for
the numerical estimation of rodenticide density (NERD).
The NERD algorithm performs calculations with increased accuracy, displaying results almost in real-time.
NERD describes the relationship between bait density, the mass flow rate of rodenticide through the
bait bucket, and helicopter speed and produces maps of bait density on the ground.
NERD also facilitates the planning of helicopter flight paths and allows for the instant
identification of areas with low or high bait density.

## Installation 🏗️

To install from pip:

```bash
pip install geci-nerd
```

or clone directly from Github

```bash
git clone git@github.com:IslasGECI/nerd.git

cd nerd
```

and install from source

```bash
pip install --editable .
```

`geci-nerd` is developed under Python >= 3.8. 🐍

## Jupyter Notebook Demonstrations 📒

You can explore the functionality of NERD through interactive Jupyter notebooks.
These are the options to access the demonstration notebooks:

- View a static version on GitHub.
  Simply navigate to the [calibration-demo](https://github.com/IslasGECI/nerd/blob/develop/examples/calibration-demo.ipynb) and [tiling_demo](https://github.com/IslasGECI/nerd/blob/develop/examples/tiling_demo.ipynb) notebooks.
- Alternatively, you can run the Jupyter notebooks locally using Docker.
  Follow the instructions below:

First, pull the latest demo image:

```shell
docker pull islasgeci/nerd_demo:latest
```

Then, run the container:

```shell
docker run --detach --publish 8080:8888 --rm islasgeci/nerd_demo
```

Lastly, explore the Jupyter notebooks at http://localhost:8080/

## References ✏️

- Rojas-Mayoral, E. (2019) «Improving the efficiency of aerial rodent eradications by means of the numerical estimation of rodenticide density». Island invasives: scaling up to meet the challenge, IUCN. [doi: 10.5281/zenodo.10214344.](https://doi.org/10.5281/zenodo.10214344)

---
## Author
- [Grupo de Ecología y Conservación de Islas](https://www.islas.org.mx/)

## Contributors
<a href="https://github.com/IslasGECI/nerd/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=IslasGECI/nerd" />
</a>

### Guidelines
- [Contributing to nerd](CONTRIBUTING.md)
