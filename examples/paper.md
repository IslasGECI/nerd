---
title: 'NERD: Numerical Estimation of Rodenticide Density'
tags:
  - aerial broadcast
  - bait bucket
  - Python
  - rodent eradication
  - rodenticide bait density
authors:
  - name: Evaristo Rojas-Mayoral
    orcid: 0000-0001-6812-9562
    corresponding: true
    affiliation: 1
  - name: Braulio Rojas-Mayoral
    orcid: 0000-0003-2358-2843
    affiliation: 1
  - name: Federico A. Méndez-Sánchez
    orcid: 0000-0002-3467-0008
    affiliation: 1
affiliations:
  - name: Grupo de Ecología y Conservación de Islas
    index: 1
bibliography: references.bib

...

# Summary

Invasive rodents are present on approximately 90% of the world's islands and constitute one of the most serious threats to both endemic and native island species. The eradication of rodents is central to island conservation efforts and the aerial broadcast of rodenticide bait is the preferred dispersal method. To maximize the efficiency of rodent eradication campaigns utilizing aerial dispersal methods, the generation of accurate and real-time bait density maps are needed.
Traditionally, the creation of ground-level bait dispersion maps has relied on Geographic Information System (GIS), an approach that is time-consuming and based on untested assumptions. In order to improve accuracy and expedite the evaluation of aerial operations, we developed an algorithm called NERD: Numerical Estimation of Rodenticide Density, which performs calculations with high precision and provides immediate results. At its core, NERD is a probability density function describing the bait density on the ground as a function of the aperture diameter of the bait bucket and the helicopter speed. The effectiveness of the model was demonstrated through its successful utilization in two rodent eradication campaigns in Mexico: the mice eradication on San Benito Oeste Island (400 ha) in the Mexican Pacific, and the ship rat eradication on Cayo Centro Island (539 ha) from Banco Chinchorro, in the Mexican Caribbean. Notably, the latter campaign represents the largest rodent eradication on a wet tropical island to date. NERD's efficacy has been proven, and it has the potential to significantly reduce the overall cost of large-scale rodent eradication campaigns.

# Introduction

The effects of invasive rodent species on island ecosystems are incredibly deleterious, especially
on islands that present high levels of endemism and islands that have evolved in the absence of
predators occupying similar niches to the invasive rodent species or higher order predators
[@Meyers2000]. The population biology of invasive rodents on islands is still poorly understood [Grant2015], but the presence of rodents on islands can lead to the rapid decline, severe reduction and extinction of native plant and animal species [@Medina2011; @Towns2006]. The resultant losses are reflected in reduced biodiversity on the affected islands and in many cases, the emergence of the invasive rodent as the dominant species. In severe cases of rodent invasion, key island ecosystem services are lost [@Towns2006]. 
As such, the first step in island restoration and biodiversity recovery is the eradication of invasive rodent species. Effective strategies have been developed to combat the detrimental effects of invasive rodent species on island ecosystems. These strategies are designed to minimize or eradicate rodent populations, thereby facilitating the restoration of native species and the reestablishment of crucial ecosystem processes. One widely utilized strategy is the aerial broadcast of rodenticide bait, which involves dispersing bait pellets from helicopters over the targeted areas. This method has proven to be highly effective in reducing rodent populations and has been successfully employed in numerous eradication campaigns [@Keitt2015].

# Statement of need

Of the various means of rodent eradication on islands, the aerial broadcast of rodenticide bait is
one of the preferred methods given the obvious advantages. The aerial dispersal of rodenticide can
cover large areas quickly and can mitigate the challenges associated with complex topography. To
assess the effectiveness of an aerial operation, bait density maps are required to evaluate the
spatial variation of bait availability on the ground. However, creating bait density maps has been
traditionally slow and impractical in the field, while taking in situ measurements to evaluate
aerial work is difficult given the challenges associated with field conditions, topography, and
available labor force.

To address these challenges, we have developed NERD: Numerical Estimation of Rodenticide Dispersal.
NERD facilitates the evaluation of helicopter rodenticide dispersal campaigns by generating bait
density maps automatically and allowing for the instant identification of bait gaps with fewer in
situ measurements. The algorithm is based on prior calibration experiments
in which the mass flow of rodenticide through a bait bucket is measured. At its core, NERD is a
probability density function that describes the bait density on the ground as a function of the bucket aperture diameter and the helicopter speed.

# Formulation

@Mayoral-Rojas2019 showed that the function $\sigma(x,y)$ used to represent the
superficial bait density (kg/m$^2$), must comply with the following property:
\begin{equation}
\int_{-\frac{w}{2}}^{+\frac{w}{2}} \sigma(x)dx=\frac{\dot{m}}{s}
  \label{eq:integralDeDensidadEsflujoSobreRapidez}
\end{equation}
where $\dot{m}$ is the bait flow (kg/s), $s$ is the speed of the helicopter (m/s), and $w$ is the swath width (m).

# Calibration

Assuming the density is independent of $x$, i.e. $\sigma$ does not change along the swath width,
equation \eqref{eq:integralDeDensidadEsflujoSobreRapidez} can be easily solved to obtain:

\begin{equation}
  \sigma = \frac{\dot{m}}{s\cdot w}.
  \label{eq:densidadEsFlujoSobreProductoRapidezPorAncho}
\end{equation}



In order to write equation \eqref{eq:densidadEsFlujoSobreProductoRapidezPorAncho} as a function of
the aperture diameter of the bait bucket, we express the mass flow rate of bait as a function of the
aperture diameter, $\dot{m}(d)$. To do this, the bait in the bucket was weighed and the time
required to empty the bucket was measured and repeated using several aperture diameters. Figure
\ref{fig:flujoDeApertura} shows the results from the calibration as well as the fitted model.


```python
import nerd
import nerd.calibration
import nerd.density_functions
```


```python
%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
```

## Fit flow rate


```python
flow_data = pd.read_csv("/workdir/data/flow.csv")
flow_data = flow_data[flow_data.bait_status == "new"][["aperture", "flow"]]
```


```python
aperture_diameters = flow_data.aperture.values
flow_rates = flow_data.flow.values
flow_rate_function = nerd.calibration.fit_flow_rate(aperture_diameters, flow_rates)
```


```python
x = np.linspace(min(aperture_diameters) - 10, max(aperture_diameters) + 10)
y = flow_rate_function(x)
fontsize = 15

plt.plot(x, y)
plt.plot(aperture_diameters, flow_rates, "o", markeredgecolor="k")
plt.xlabel("Aperture diameter (mm)", size=fontsize)
plt.ylabel("Mass flow rate (kg/s)", size=fontsize)
plt.xlim(50, 100)
plt.ylim(0, 3)
plt.xticks(size=fontsize)
plt.yticks(size=fontsize)
plt.savefig("figures/calibration.png", dpi=300, transparent=True)
```


    
![png](paper_files/paper_15_0.png)
    


![Flow rate $\dot{m}$ (kg/s) as a function of aperture diameter, $d$ (mm); each symbol represents a
calibration event and the black curve is the quadratic model fitted to the data.\label{fig:calibration}]("figures/calibration.png")

## Swath width


```python
density_profile = pd.read_csv("/workdir/data/profile.csv")
```


```python
distance = density_profile.distance.values
density_kg_per_ha = density_profile.density.values
density = density_kg_per_ha / 1e4  # To convert densities to kg per square meter
swath_width = nerd.calibration.get_swath_width(distance, density)
```


```python
size = 10
fontsize = 15
plt.plot(distance, density_kg_per_ha, "o")
plt.xlabel("Position from flightpath (m)", size=fontsize)
plt.ylabel("Bait Density (kg/ha)", size=fontsize)
plt.xlim(-40, 40)
plt.ylim(0, 6)
plt.xticks(size=size)
plt.yticks(size=size)
plt.text(
    -0.5,
    3,
    "Flightpath",
    size=15,
    color="k",
    rotation=90,
    bbox=dict(facecolor="w", edgecolor="none"),
)
plt.axvline(0, color="k")
plt.savefig("figures/plots.png", dpi=300, transparent=True)
```


    
![png](paper_files/paper_20_0.png)
    


![Aca va el pie de figura.\label{fig:plots}]("figures/plots.png")

## Select best density function


```python
aperture_diameter_data = 55  # milimetres
helicopter_speed_data = 20.5778  # meters per second (40 knots)
```


```python
density_function = nerd.calibration.get_best_density_function(
    distance,
    density,
    aperture_diameter_data,
    helicopter_speed_data,
    swath_width,
    flow_rate_function,
)
estimated_profile = nerd.solver(
    aperture_diameter_data,
    helicopter_speed_data,
    swath_width,
    density_function,
    flow_rate_function,
)
```


```python
fontsize = 15
x = np.linspace(min(distance), max(distance))
y = estimated_profile(x)
estimated_density = estimated_profile(distance)
plt.figure(figsize=[11, 8])
plt.plot(x, y, "r", label="estimated density")
plt.vlines(distance, density, density + estimated_density - density, "k")
plt.plot(
    distance,
    density,
    "s",
    color="orange",
    markeredgecolor="black",
    label="real density",
)
plt.xlabel("Distance (m)", size=fontsize)
plt.ylabel("Density (kg/m$^2$)", size=fontsize);
plt.savefig("figures/density_profile.png")
```


    
![png](paper_files/paper_25_0.png)
    


![Aca va el pie de figura.\label{fig:density_profile}]("figures/density_profile.png")

## Calibration model


```python
aperture_diameters_domain = np.linspace(min(aperture_diameters), max(aperture_diameters))
helicopter_speeds_domain = np.linspace(10, 50)
density_matrix = nerd.calibration.model(
    aperture_diameters_domain,
    helicopter_speeds_domain,
    swath_width,
    nerd.density_functions.uniform,
    flow_rate_function,
)
conversion_factor_ms_to_kmh = 3.6
helicopter_speed_kmh = helicopter_speeds_domain * conversion_factor_ms_to_kmh
```


```python
fontsize_ticks = 10
fontsize_labels = 15
fontsize_textlabels = 25
fig, ax = plt.subplots(figsize=(20, 10))
color_contour = ax.contourf(
    aperture_diameters_domain,
    helicopter_speeds_domain,
    density_matrix * 1e4,
    zorder=0,
    vmin=0,
    vmax=20,
)
line_contour = ax.contour(
    aperture_diameters_domain,
    helicopter_speeds_domain,
    density_matrix * 1e4,
    levels=color_contour.levels,
    colors="k",
)
cbar = fig.colorbar(color_contour)
ax.clabel(line_contour, line_contour.levels, inline=True, fontsize=20, fmt="%1.0f")
plt.xlabel("Aperture diameter (mm)", size=fontsize_textlabels)
plt.ylabel("Helicopter speed (km/h)", size=fontsize_textlabels)
ytickslocs = ax.get_yticks()
y_ticks_kmh = ytickslocs * 3.6
plt.yticks(ytickslocs, y_ticks_kmh.astype(int), size=fontsize_ticks)
plt.xticks(size=fontsize_ticks)
cbar.ax.set_ylabel("Density (kg/ha)", size=fontsize_labels)
cbar.ax.tick_params(labelsize=fontsize_ticks)
plt.axhline(18.0056, color="r", linewidth=2)
plt.text(65, 18.6, "35 knot", size=fontsize_labels, color="k")
plt.savefig("figures/contour_plot.png", dpi=300, transparent=True)
```


    
![png](paper_files/paper_29_0.png)
    


![\ref{fig:contour_plot} Surface bait density $\sigma$ (kg/ha) as a function of aperture
diameter $d$ (mm), and speed $s$ (km/hr). The horizontal axis shows the aperture diameter of the
bait bucket and the vertical axis shows the helicopter's speed. The resulting bait density on the
ground is shown in the second vertical color axis. $\sigma(d,s)= \frac{\dot{m}(d)}{s\cdot w}$.
\label{fig:contour_plot}]("figures/contour_plot.png")

The resulting three-dimensional model, $$\sigma(d,s)= \frac{\dot{m}(d)}{s\cdot w},$$ is shown in
Figure \ref{fig:densidadDeAperturaYRapidez}. During the planning stage of an eradication campaign,
this model can be used to determine the diameter of the bait bucket needed to achieve the desired
bait density on the ground, ensuring efficient bait coverage, while maximizing resources, time and
labor force.


```python

```

# Application

For a given island, a particular bait density is required on the ground for a successful rodent
eradication. This density is determined after studying the ecosystems of the island and the biology
of the invasive target species. Given the required bait density and the total area of the island,
the minimum amount of bait needed for the eradication operation can be calculated using NERD. While
planning helicopter flights paths, it is assumed that the bait density within each swath is
constant, but variable between swaths.

Assuming a variable bait density along each swath but uniform density across the swath, we can
estimate bait density with greater precision after the aerial dispersal given that the bait density
for each cell is calculated between two consecutive points recorded by the GPS. This case considers
the effects on density when the helicopter flies with variable speed (Figure
\ref{fig:densidadSimetrica}).

To account for the well known fact that we have a higher density of rodenticide right bellow of the
helicopter and lower densities along the edges of the swath, we can assume a variable bait density
both along and across each swath.  This allows for the detection of areas where the bait density is
below the lower limit of the target bait density or of gaps on the ground without any bait.

## Tiling demo


```python
from nerd.io import Nerd
from nerd.density_functions import normal
import matplotlib.pyplot as plt

%matplotlib inline
plt.rcParams["figure.figsize"] = (10, 10)
```

# Setting up field parameters


```python
from nerd.io import Nerd
```


```python
config_filepath = "/workdir/data/nerd_config.json"
```


```python
nerd_model = Nerd(config_filepath)
nerd_model.calculate_total_density()
density_map = nerd_model.export_results_geojson(target_density=0.002)
plt.savefig("figures/density_map.png")
```

    100%|██████████| 6269/6269 [01:33<00:00, 66.83it/s] 



    
![png](paper_files/paper_41_1.png)
    


![Aca va el pie de figura.\label{fig:density_map}]("figures/density_map.png")

# Discussion

NERD is an algorithm, based on past calibration experiments in which the mass flow of bait through a bait bucket is measured, that describes bait density as a function of the aperture diameter and the helicopter
speed. NERD can assist in the planning of the aerial operations as well as during the eradication,
giving near real-time feedback allowing for on-the-spot corrections during the operation. The final
product of NERD is a bait density map generated in a matter of seconds, that allows for the
instant identification of bait gaps and the efficient use of resources.

# References
