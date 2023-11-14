#!/usr/bin/env python
# coding: utf-8

# # Application
# 
# For a given island, a particular bait density is required on the ground for a successful rodent
# eradication. This density is determined after studying the ecosystems of the island and the biology
# of the invasive target species. Given the required bait density and the total area of the island,
# the minimum amount of bait needed for the eradication operation can be calculated using NERD. While
# planning helicopter flights paths, it is assumed that the bait density within each swath is
# constant, but variable between swaths.

# Assuming a variable bait density along each swath but uniform density across the swath, we can
# estimate bait density with greater precision after the aerial dispersal given that the bait density
# for each cell is calculated between two consecutive points recorded by the GPS. This case considers
# the effects on density when the helicopter flies with variable speed (Figure
# \ref{fig:densidadSimetrica}).

# To account for the well known fact that we have a higher density of rodenticide right bellow of the
# helicopter and lower densities along the edges of the swath, we can assume a variable bait density
# both along and across each swath.  This allows for the detection of areas where the bait density is
# below the lower limit of the target bait density or of gaps on the ground without any bait.

# ## Tiling demo

# In[1]:


from nerd.io import Nerd
from nerd.density_functions import normal
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams["figure.figsize"] = (10, 10)


# # Setting up field parameters

# In[2]:


from nerd.io import Nerd


# In[3]:


config_filepath = "/workdir/data/nerd_config.json"


# In[4]:


nerd_model = Nerd(config_filepath)
nerd_model.calculate_total_density()
density_map = nerd_model.export_results_geojson(target_density=0.002)
plt.savefig("/workdir/figures/density_map.png")


# ![Aca va el pie de figura.\label{fig:density_map}]("figures/density_map.png")

# # Discussion
# 
# NERD is an algorithm, based on past calibration experiments in which the mass flow of bait through a bait bucket is measured, that describes bait density as a function of the aperture diameter and the helicopter
# speed. NERD can assist in the planning of the aerial operations as well as during the eradication,
# giving near real-time feedback allowing for on-the-spot corrections during the operation. The final
# product of NERD is a bait density map generated in a matter of seconds, that allows for the
# instant identification of bait gaps and the efficient use of resources.

# # References
