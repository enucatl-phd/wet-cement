import click
import numpy as np
import h5py
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from tqdm import tqdm


@click.command()
@click.argument("input_files", nargs=-1)
def main(input_files):
    FFMpegWriter = manimation.writers["avconv"]
    metadata = {
        "title": "Movie test",
    }
    writer = FFMpegWriter(fps=10, metadata=metadata)
    figure = plt.figure()
    input_files = input_files[:300]
    with writer.saving(figure, "writer_test.mp4", 100):
        for input_file in tqdm(input_files):
            h5file = h5py.File(input_file)
            reconstruction = h5file["postprocessing/dpc_reconstruction"][...]
            min_x = 0
            max_x = -1
            min_y = 200
            max_y = 400
            dark_field = reconstruction[min_y:max_y, min_x:max_x, 2]
            absorption = reconstruction[min_y:max_y, min_x:max_x, 0]
            dataset = np.log(dark_field) / np.log(absorption)
            limits = stats.mstats.mquantiles(dataset, prob=[0.1, 0.9])
            image = plt.imshow(dataset, interpolation="none")
            image.set_clim(*limits)
            writer.grab_frame()


if __name__ == "__main__":
    main()
