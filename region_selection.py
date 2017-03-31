import click
import h5py
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib import path
import csv
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        with h5py.File(output_file, "w") as output_h5_file:
            for i, dataset_name in enumerate(tqdm(input_h5_file)):
                dataset = input_h5_file[dataset_name][..., 2]
                if i == 0:
                    fig, ax = plt.subplots()
                    # limits = [0.7, 1]
                    limits = stats.mstats.mquantiles(dataset, prob=[0.1, 0.9])
                    print(limits)
                    image = ax.imshow(dataset, interpolation="none", aspect='auto')
                    image.set_clim(*limits)
                    xv, yv = np.meshgrid(
                        np.arange(dataset.shape[0]),
                        np.arange(dataset.shape[1])
                    )
                    pix = np.transpose(np.vstack(
                        (yv.flatten(), xv.flatten())
                    ))

                    def onselect(verts):
                        global ind
                        p = path.Path(verts)
                        ind = p.contains_points(pix, radius=1)
                        ind = np.reshape(ind, dataset.shape, order="F")

                    plt.ion()
                    lasso = LassoSelector(ax, onselect, lineprops={"color": "red"})
                    plt.show()
                    input('Press any key to accept selected points')
                output_h5_file[dataset_name] = dataset[ind]


if __name__ == "__main__":
    main()
