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

Invasive rodents are present on approximately 90% of islands worldwide, seriously threatening endemic and native island species and making rodent eradication central to island conservation. Aerial broadcast is the preferred dispersal method of rodenticide bait. 
Therefore, accurate bait density maps must be generated in real-time to maximize the efficiency of rodent eradication campaigns utilizing aerial dispersal methods. 
Traditionally, conservationists rely on ground-level bait dispersion maps generated using Geographic Information Systems (GIS). 
However, this approach is time-consuming and based on untested assumptions. 
To improve the accuracy and efficiency of aerial operations, we developed NERD (Numerical Estimation of Rodenticide Density), an algorithm that performs highly precise calculations and provides immediate results. 
At its core, NERD  is a probability density function describing bait density on the ground as a function of the aperture diameter of the rodenticide bucket and helicopter speed. 
We have confirmed the effectiveness of the model by successfully utilizing it in two island rodent eradication campaigns: mice eradication on San Benito Oeste (400 ha) in the Mexican Pacific and ship rat eradication on Cayo Centro (539 ha) of Banco Chinchorro in the Mexican Caribbean. 
Notably, the Cayo Centro campaign is the largest rodent eradication ever conducted on a wet tropical island to date. We have proved the efficiency of NERD and its potential to reduce the overall cost of large-scale rodent eradication campaigns significantly.

# Introduction

Invasive rodent species are incredibly deleterious to island ecosystems, especially those with levels of endemism or those without higher-order predators or predators occupying similar niches to the invasive rodents [@Meyers2000]. 
Invasive rodent population dynamics are poorly understood on islands [@Harper2015]. 
However, rodents on islands can cause native plant and animal species to decline rapidly and severely, even to extinction [@Medina2011; @Towns2006]. 
The resultant losses are reflected in reduced biodiversity and, in many cases, invasive rodents becoming the dominant species. 
In cases of severe rodent invasion, critical island ecosystem services are lost [@Towns2006]. 
The first step to resorting to islands and recovering biodiversity is eradicating invasive rodents.
Effective strategies to combat the detrimental effects of invasive rodent species on island ecosystems aim to minimize or eradicate rodent populations, facilitating the restoration of native species and crucial ecosystem processes. 
The aerial broadcast of rodenticide is widely utilized and involves dispersing rodenticide bait pellets from helicopters over target areas. 
Aerial broadcast effectively reduces rodent populations and has been successfully employed in numerous eradication campaigns [@Keitt2015].

# Statement of need

Aerial rodenticide broadcast is the preferred method to eradicate invasive island species because of its obvious advantages. Aerial broadcast can quickly cover large areas with bait, mitigating the challenges associated with navigating complex topography by land. 
Bait density maps that show the spatial variation in availability on the ground are necessary to assess the effectiveness of aerial operations. 
However, creating bait density maps is traditionally slow and impractical in the field. 
Moreover, taking in situ measurements to evaluate aerial rodenticide broadcasts can be challenging due to field conditions, topography, and labor required.

We developed NERD (Numerical Estimation of Rodenticide Dispersal) to address these challenges. NERD generates bait density maps automatically, allowing for the instant identification of bait gaps with fewer in situ measurements and facilitating the evaluation of helicopter rodenticide dispersal campaigns. 
NERD requires prior calibration experiments to determine the mass flow of rodenticide through the bait bucket. 
At its core, NERD is a probability density function that describes bait density on the ground as a function of the bucket aperture diameter and helicopter speed.

# Formulation

@Rojas2019 showed that the function $\sigma(x,y)$ to represent superficial bait density (kg/m$^2$) must comply with the following property:
\begin{equation}
\int_{-\frac{w}{2}}^{+\frac{w}{2}} \sigma(x)dx=\frac{\dot{m}}{s},
  \label{eq:integralDeDensidadEsflujoSobreRapidez}
\end{equation}
where $\dot{m}$ is the bait flow (kg/s), $s$ is the speed of the helicopter (m/s), and $w$ is the swath width (m).

# Calibration

Assuming the density is independent of $x$ (i.e., $\sigma$ does not change along the swath width) and expressing the mass flow rate of the bait as a function of the aperture diameter, $\dot{m}(d)$, we obtain a two-parameter model:

\begin{equation} \sigma(d,s)= \frac{\dot{m}(d)}{s\cdot w}. \end{equation}

We obtained the mass flow rate as a function of the aperture diameter of the bait bucket by measuring the time required to empty the bucket. 
We repeated this using several aperture diameters and a known initial mass.


```python
import nerd
import nerd.calibration
import nerd.density_functions
```


```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
```

## Fit flow rate


```python
flow_data = pd.read_csv("/workdir/tests/data/flow.csv")
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
plt.savefig("examples/figures/calibration.png", dpi=300, transparent=True)
```



![Flow rate $\dot{m}$ (kg/s) as a function of the aperture diameter [$d$ (mm)]. Each dot represents a calibration even. The blue line is the quadratic model fitted to the data.\label{fig:calibration}](figures/calibration.png)

## Swath width


```python
density_profile = pd.read_csv("/workdir/tests/data/profile.csv")
```


```python
distance = density_profile.distance.values
density_kg_per_ha = density_profile.density.values
density = density_kg_per_ha / 1e4  # To convert densities to kg per square meter
swath_width = nerd.calibration.get_swath_width(distance, density)
```


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
plt.savefig("examples/figures/density_profile.png")
```
Figure \ref{fig:density_profile} shows the relationship between the bait density and parameters following calibration.

We can assume a variable bait density across each swath to account for the higher density of rodenticide below the helicopter compared to the lower density along the edges of the swath. 
In doing so, we can detect areas with bait density below the lower limit of the target bait density and bait gaps on the ground.


![Bait density $\sigma$ (kg/ha) as a function of the distance from the flight path (m). The dots show the measured density on the ground after a calibration event. The red line shows the fitted density model. \label{fig:density_profile}](figures/density_profile.png)

## Density as function of speed and aperture diameter size

From the calibration, we obtain Figure \ref{fig:contour_plot}.

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
plt.savefig("examples/figures/contour_plot.png", dpi=300, transparent=True)
```


    
    


![Surface bait density $\sigma$ (kg/ha) on the color axis as a function of the aperture diameter $d$ (mm) of the bait bucket on the horizontal axis and the helicopter speed $s$ (km/hr) on the vertical axis. \label{fig:contour_plot}](figures/contour_plot.png)

## Demonstration using a configuration file

There is another way to setup the model parameters using a json file.


```python
from nerd.io import Nerd
```


```python
config_filepath = "/workdir/tests/data/nerd_config.json"
```


```python
plt.figure(figsize=[11, 8])
nerd_model = Nerd(config_filepath)
nerd_model.calculate_total_density()
density_map = nerd_model.export_results_geojson(target_density=0.002)
plt.savefig("examples/figures/density_map.png")
```

![Bait density map after aerial rodenticide broadcast.\label{fig:density_map}](figures/density_map.png)

# Use cases

Each island requires a specific bait density to eradicate invasive rodents successfully, which requires studying the ecosystem and biology of the target species.

NERD is extremely useful when planning an eradication campaign because it can ensure efficient bait coverage while maximizing resources, time, and labor requirements.
For example, we can use NERD to determine the bait bucket diameter necessary to achieve the desired bait density on the ground.
While planning helicopter flight paths, bait density is assumed to be constant within each swath but variable between swaths.

NERD is also incredibly useful during an eradication campaign. Notably, conservationists can use NERD to generate bait density maps in nearly real-time. 
Notably, we can evaluate bait density on the ground, even when the helicopter flies at variable speeds.
The NERD maps can identify bait gaps during eradication campaigns in the field, ensuring an efficient use of resources.


# Conclusions

NERD is an algorithm that describes bait density as a function of the aperture diameter and helicopter speed, based on past calibration experiments measuring rodenticide mass flow through a bait bucket.
NERD can aid in planning aerial operations and during eradication campaigns by providing near real-time feedback and allowing for on-the-spot corrections. 
The final product of NERD is a bait density map generated in a matter of seconds, allowing for the instant identification of bait gaps and ensuring efficient resource use.

# References
