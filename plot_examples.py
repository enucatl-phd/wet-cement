#!/usr/bin/env python
# encoding: utf-8

"""Nice plot of the three DPC images"""

import os
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import click


pgf_with_rc_fonts = {
    "image.origin": "upper",
    "font.family": "serif",
    "pgf.rcfonts": False,
    "ytick.major.pad": 5,
    "xtick.major.pad": 5,
    "font.size": 11,
    "legend.fontsize": "medium",
    "axes.labelsize": "medium",
    "axes.titlesize": "medium",
    "ytick.labelsize": "medium",
    "xtick.labelsize": "medium",
    "axes.linewidth": 1,
}

mpl.rcParams.update(pgf_with_rc_fonts)


@click.command()
@click.command("input_file", type=click.Path(exists=True))
@click.command("output_file")
@click.command("index", type=int)
def main(input_file, output_file, index):
    with h5py.File(input_file, "r") as input_h5_file:
        dataset = list(input_h5_file.keys())[index]
        plt.figure()
        _, (abs_plot, ratio_plot) = plt.subplots(1, 2)
        plt.subplots_adjust(
            wspace=0.02,
            hspace=0.02)
        abs_image = abs_plot.imshow(
            dataset[..., 0],
            interpolation="none")
        abs_limits = [0.35, 0.55]
        abs_image.set_clim(*abs_limits)
        plt.colorbar(abs_image, ax=abs_plot)
        ratio_image = ratio_plot.imshow(
            dataset[..., 0],
            interpolation="none")
        ratio_limits = 
