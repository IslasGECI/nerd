#!/usr/bin/env python
# coding: utf-8

# ---
# title: 'NERD: Numerical Estimation of Rodenticide Density'
# tags:
#   - aerial broadcast
#   - bait bucket
#   - Python
#   - rodent eradication
#   - rodenticide bait density
# authors:
#   - name: Evaristo Rojas-Mayoral
#     orcid: 0000-0001-6812-9562
#     corresponding: true
#     affiliation: 1
#   - name: Braulio Rojas-Mayoral
#     orcid: 0000-0003-2358-2843
#     affiliation: 1
#   - name: Federico A. Méndez-Sánchez
#     orcid: 0000-0002-3467-0008
#     affiliation: 1
# affiliations:
#   - name: Grupo de Ecología y Conservación de Islas
#     index: 1
# bibliography: references.bib
# 
# ...

# # Summary
# 
# Invasive rodents are present on approximately 90% of the world's islands and constitute one of the most serious threats to both endemic and native island species. The eradication of rodents is central to island conservation efforts and the aerial broadcast of rodenticide bait is the preferred dispersal method. To maximize the efficiency of rodent eradication campaigns utilizing aerial dispersal methods, the generation of accurate and real-time bait density maps are needed.
# Traditionally, the creation of ground-level bait dispersion maps has relied on Geographic Information System (GIS), an approach that is time-consuming and based on untested assumptions. In order to improve accuracy and expedite the evaluation of aerial operations, we developed an algorithm called NERD: Numerical Estimation of Rodenticide Density, which performs calculations with high precision and provides immediate results. At its core, NERD is a probability density function describing the bait density on the ground as a function of the aperture diameter of the bait bucket and the helicopter speed. The effectiveness of the model was demonstrated through its successful utilization in two rodent eradication campaigns in Mexico: the mice eradication on San Benito Oeste Island (400 ha) in the Mexican Pacific, and the ship rat eradication on Cayo Centro Island (539 ha) from Banco Chinchorro, in the Mexican Caribbean. Notably, the latter campaign represents the largest rodent eradication on a wet tropical island to date. NERD's efficacy has been proven, and it has the potential to significantly reduce the overall cost of large-scale rodent eradication campaigns.

# # Introduction
# 
# The effects of invasive rodent species on island ecosystems are incredibly deleterious, especially
# on islands that present high levels of endemism and islands that have evolved in the absence of
# predators occupying similar niches to the invasive rodent species or higher order predators
# [@Meyers2000]. The population biology of invasive rodents on islands is still poorly understood [Grant2015], but the presence of rodents on islands can lead to the rapid decline, severe reduction and extinction of native plant and animal species [@Medina2011; @Towns2006]. The resultant losses are reflected in reduced biodiversity on the affected islands and in many cases, the emergence of the invasive rodent as the dominant species. In severe cases of rodent invasion, key island ecosystem services are lost [@Towns2006]. 
# As such, the first step in island restoration and biodiversity recovery is the eradication of invasive rodent species. Effective strategies have been developed to combat the detrimental effects of invasive rodent species on island ecosystems. These strategies are designed to minimize or eradicate rodent populations, thereby facilitating the restoration of native species and the reestablishment of crucial ecosystem processes. One widely utilized strategy is the aerial broadcast of rodenticide bait, which involves dispersing bait pellets from helicopters over the targeted areas. This method has proven to be highly effective in reducing rodent populations and has been successfully employed in numerous eradication campaigns [@Keitt2015].

# # Statement of need
# 
# Of the various means of rodent eradication on islands, the aerial broadcast of rodenticide bait is
# one of the preferred methods given the obvious advantages. The aerial dispersal of rodenticide can
# cover large areas quickly and can mitigate the challenges associated with complex topography. To
# assess the effectiveness of an aerial operation, bait density maps are required to evaluate the
# spatial variation of bait availability on the ground. However, creating bait density maps has been
# traditionally slow and impractical in the field, while taking in situ measurements to evaluate
# aerial work is difficult given the challenges associated with field conditions, topography, and
# available labor force.

# To address these challenges, we have developed NERD: Numerical Estimation of Rodenticide Dispersal.
# NERD facilitates the evaluation of helicopter rodenticide dispersal campaigns by generating bait
# density maps automatically and allowing for the instant identification of bait gaps with fewer in
# situ measurements. The algorithm is based on prior calibration experiments
# in which the mass flow of rodenticide through a bait bucket is measured. At its core, NERD is a
# probability density function that describes the bait density on the ground as a function of the bucket aperture diameter and the helicopter speed.

# # Formulation
# 
# @Mayoral-Rojas2019 showed that the function $\sigma(x,y)$ used to represent the
# superficial bait density (kg/m$^2$), must comply with the following property:
# \begin{equation}
# \int_{-\frac{w}{2}}^{+\frac{w}{2}} \sigma(x)dx=\frac{\dot{m}}{s}
#   \label{eq:integralDeDensidadEsflujoSobreRapidez}
# \end{equation}
# where $\dot{m}$ is the bait flow (kg/s), $s$ is the speed of the helicopter (m/s), and $w$ is the swath width (m).

# # Calibration
# 
# Assuming the density is independent of $x$, i.e. $\sigma$ does not change along the swath width,
# equation \eqref{eq:integralDeDensidadEsflujoSobreRapidez} can be easily solved to obtain:

# \begin{equation}
#   \sigma = \frac{\dot{m}}{s\cdot w}.
#   \label{eq:densidadEsFlujoSobreProductoRapidezPorAncho}
# \end{equation}

# 
