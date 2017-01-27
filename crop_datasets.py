import h5py
import numpy as np
import click
import matplotlib.pyplot as plt
import os


@click.command()
@click.argument("inputname", type=click.Path(exists=True))
def main(inputname):
    min_x = 350
    min_y = 550
    max_x = 750
    max_y = 1000
    datasets = []
    with h5py.File(outputname) as outh5file:
        with h5py.File(inputname, "r") as h5file:
            group = h5file["/entry/data"]
            outputgroup = outh5file["/entry/data"]
            for dataset in group:
                new_dataset = group[dataset][min_y:max_y, min_x:max_x]
                plt.imshow(new_dataset)
                plt.ion()
                plt.show()
                input()
                outputgroup[dataset] = new_dataset


if __name__ == "__main__":
    main()
