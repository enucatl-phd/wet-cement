import click
import numpy as np
import h5py
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        FFMpegWriter = manimation.writers["avconv"]
        metadata = {
            "title": "concrete sample",
        }
        writer = FFMpegWriter(fps=5, metadata=metadata)
        figure = plt.figure()
        ax = figure.add_subplot(111)
        plt.tight_layout()
        dataset_names = list(input_h5_file.keys())[0:20]
        abs_dataset = input_h5_file[dataset_names[0]][..., 0]
        ratio_dataset = input_h5_file[dataset_names[0]][..., 2]
        limits = [
            [0.35, 0.55],
            [0.3, 0.45],
            [0.5, 2],
        ]
        im = ax.imshow(
            abs_dataset,
            interpolation="none",
            clim=limits[0])
        cbar = figure.colorbar(im, ax=ax)
        ratio_ax = plt.add_subplot(112)
        ratio_im = ratio_ax.imshow(
            ratio_dataset,
            interpolation="none",
            clim=limits[2])
        ratio_cbar = figure.colorbar(ratio_im, ax=ratio_ax)

        def update_img(dataset_name):
            abs_dataset = input_h5_file[dataset_name][..., 0]
            ratio_dataset = input_h5_file[dataset_name][..., 2]
            im.set_data(abs_dataset)
            ratio_im.set_data(ratio_dataset)

        ani = manimation.FuncAnimation(
            figure,
            update_img,
            tqdm(dataset_names),
            interval=100)

        dpi=120
        writer = manimation.writers["avconv"](fps=30)
        ani.save(output_file, writer=writer, dpi=dpi)
            

if __name__ == "__main__":
    main()
