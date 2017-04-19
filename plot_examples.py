#!/usr/bin/env python
# encoding: utf-8

"""Nice plot of the three DPC images"""

import os
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import ticker
import datetime
import click
from mpl_toolkits.axes_grid1 import make_axes_locatable


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
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
@click.option("-n", type=int)
def main(input_file, output_file, n):
    with h5py.File(input_file, "r") as input_h5_file:
        dataset_name_list = list(input_h5_file.keys())
        dataset_name = dataset_name_list[n]
        dataset = input_h5_file[dataset_name]

        time = datetime.datetime.strptime(
            dataset_name, "%y%m%d.%H%M%S%f")
        time0 = datetime.datetime.strptime(
            dataset_name_list[0], "%y%m%d.%H%M%S%f")
        time_delta = (time - time0).total_seconds()
        time_delta_hours = int(time_delta // 3600)
        time_delta_minutes = int((time_delta % 3600) // 60)
        width = 4
        factor = 0.618
        height = width * factor
        figure = plt.figure(figsize=(width, height))
        figure.suptitle("time = {0}h{1}m".format(
            time_delta_hours,
            time_delta_minutes
        ))
        abs_axes = figure.add_subplot(121)
        plt.subplots_adjust(
            wspace=0.02,
            hspace=0.02)
        abs_image = abs_axes.imshow(
            dataset[..., 0],
            interpolation="none")
        abs_limits = [0.35, 0.55]
        abs_image.set_clim(*abs_limits)
        abs_divider = make_axes_locatable(abs_axes)
        abs_cax = abs_divider.append_axes(
            "left", size="5%", pad=0.05)
        abs_colorbar = plt.colorbar(abs_image, cax=abs_cax)
        abs_tick_locator = ticker.MaxNLocator(nbins=4)
        abs_colorbar.locator = abs_tick_locator
        abs_colorbar.update_ticks()
        abs_cax.yaxis.set_ticks_position("left")
        abs_axes.set_title(r"$-\log(\mathrm{absorption})$")
        abs_axes.set_frame_on(False)
        abs_axes.axes.xaxis.set_ticks([])
        abs_axes.axes.yaxis.set_ticks([])
        abs_axes.add_patch(Rectangle((37, 13), 30, 5, facecolor="red"))
        abs_axes.text(52, 23, "1 mm", ha="center", va="top", color="red")
        ratio_axes = figure.add_subplot(122)
        ratio_image = ratio_axes.imshow(
            dataset[..., 2],
            interpolation="none")
        ratio_limits = [0.5, 2]
        ratio_image.set_clim(*ratio_limits)
        ratio_axes.set_title(
            r"$\frac{\log(\mathrm{dark\, field})}{\log(\mathrm{absorption})}$")
        ratio_divider = make_axes_locatable(ratio_axes)
        ratio_cax = ratio_divider.append_axes(
            "right", size="5%", pad=0.05)
        ratio_colorbar = plt.colorbar(ratio_image, cax=ratio_cax)
        ratio_tick_locator = ticker.MaxNLocator(nbins=4)
        ratio_colorbar.locator = ratio_tick_locator
        ratio_colorbar.update_ticks()
        ratio_axes.set_frame_on(False)
        ratio_axes.axes.xaxis.set_ticks([])
        ratio_axes.axes.yaxis.set_ticks([])
        plt.subplots_adjust(top=0.8)
        plt.savefig(output_file, bbox_inches="tight", dpi=300)
        # plt.show()
        # plt.ion()
        # input()


if __name__ == "__main__":
    main()
