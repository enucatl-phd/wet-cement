import h5py
import numpy as np
from scipy import stats
import click
import matplotlib.pyplot as plt
import os


@click.command()
@click.argument("inputname", type=click.Path(exists=True))
def main(inputname):
    min_x = 100
    max_x = 400
    min_y = 300
    max_y = 700
    outputname = os.path.join("data", os.path.basename(inputname))
    print(outputname)
    with h5py.File(outputname) as outh5file:
        with h5py.File(inputname, "r") as h5file:
            group = h5file["/entry/data/th_0"]
            outputgroup = outh5file.require_group("/entry/data/th_0")
            for dataset in group:
                new_dataset = group[dataset][min_y:max_y, min_x:max_x]
                # limits = stats.mstats.mquantiles(
                    # new_dataset, prob=[0.1, 0.9])
                # print(limits)
                # image = plt.imshow(new_dataset, interpolation="none", aspect='auto')
                # image.set_clim(*limits)
                # plt.ion()
                # plt.show()
                # input()
                outputgroup[dataset] = new_dataset


if __name__ == "__main__":
    main()
