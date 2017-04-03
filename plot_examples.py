#!/usr/bin/env python
# encoding: utf-8

"""Nice plot of the three DPC images"""

import os
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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
        figure = plt.figure()
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
        plt.colorbar(abs_image, cax=abs_cax)
        abs_cax.yaxis.set_ticks_position("left")
        abs_axes.set_title("log(absorption)")
        abs_axes.set_frame_on(False)
        abs_axes.axes.xaxis.set_ticks([])
        abs_axes.axes.yaxis.set_ticks([])
        ratio_axes = figure.add_subplot(122)
        ratio_image = ratio_axes.imshow(
            dataset[..., 2],
            interpolation="none")
        ratio_limits = [0.5, 2]
        ratio_image.set_clim(*ratio_limits)
        ratio_axes.set_title("log(dark field)/log(absorption)")
        ratio_divider = make_axes_locatable(ratio_axes)
        ratio_cax = ratio_divider.append_axes(
            "right", size="5%", pad=0.05)
        plt.colorbar(ratio_image, cax=ratio_cax)
        ratio_axes.set_frame_on(False)
        ratio_axes.axes.xaxis.set_ticks([])
        ratio_axes.axes.yaxis.set_ticks([])
        plt.savefig(output_file, bbox_inches="tight", dpi=120)
        # plt.show()
        # plt.ion()
        # input()


if __name__ == "__main__":
    main()
