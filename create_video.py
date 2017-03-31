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
@click.argument("index", type=int)
def main(input_file, output_file, index):
    with h5py.File(input_file, "r") as input_h5_file:
        FFMpegWriter = manimation.writers["avconv"]
        metadata = {
            "title": "concrete sample",
        }
        writer = FFMpegWriter(fps=5, metadata=metadata)
        figure = plt.figure()
        ax = figure.add_subplot(111)
        plt.tight_layout()
        dataset_names = list(input_h5_file.keys())
        test_dataset = input_h5_file[dataset_names[0]][..., index]
        limits = [
            [0.35, 0.55],
            [0.3, 0.45],
            [0.5, 2],
        ]
        im = ax.imshow(
            test_dataset,
            interpolation="none",
            clim=limits[index])
        cbar = figure.colorbar(im, ax=ax)

        def update_img(dataset_name):
            dataset = input_h5_file[dataset_name][..., index]
            im.set_data(dataset)

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
