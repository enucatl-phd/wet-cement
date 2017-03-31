import click
import h5py
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib import path
import csv
import gzip


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        with gzip.open(output_file, "wt") as output_file:
            dataset_name = list(input_h5_file.keys())[50]
            absorption_dataset = input_h5_file[dataset_name][..., 0]
            ratio_dataset = input_h5_file[dataset_name][..., 2]
            fig, ax = plt.subplots()
            # limits = [0.7, 1]
            limits = stats.mstats.mquantiles(ratio_dataset, prob=[0.1, 0.9])
            print(limits)
            image = ax.imshow(ratio_dataset, interpolation="none", aspect='auto')
            image.set_clim(*limits)
            xv, yv = np.meshgrid(
                np.arange(ratio_dataset.shape[0]),
                np.arange(ratio_dataset.shape[1])
            )
            pix = np.transpose(np.vstack(
                (yv.flatten(), xv.flatten())
            ))

            def onselect(verts):
                global ind
                p = path.Path(verts)
                ind = p.contains_points(pix, radius=1)
                ind = np.reshape(ind, ratio_dataset.shape, order="F")

            plt.ion()
            ax.set_title("select wet region")
            lasso = LassoSelector(ax, onselect, lineprops={"color": "red"})
            plt.show()
            input('Press any key to accept selected points')
            wet_ratio = ratio_dataset[ind]
            wet_absorption = absorption_dataset[ind]
            ax.set_title("select dry region")
            lasso = LassoSelector(ax, onselect, lineprops={"color": "red"})
            plt.show()
            input('Press any key to accept selected points')
            dry_ratio = ratio_dataset[ind]
            dry_absorption = absorption_dataset[ind]
            writer = csv.writer(output_file)
            writer.writerow(["status", "ratio", "absorption"])
            for r, a in zip(wet_ratio, wet_absorption):
                writer.writerow(["wet", r, a])
            for r, a in zip(dry_ratio, dry_absorption):
                writer.writerow(["dry", r, a])


if __name__ == "__main__":
    main()
