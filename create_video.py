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
    writer = FFMpegWriter(fps=5, metadata=metadata)
    figure = plt.figure()
    ax = figure.add_subplot(111)
    # input_files = input_files[:100]
    test_file = input_files[0]
    test_reconstruction = h5py.File(
        test_file)["postprocessing/dpc_reconstruction"][...]
    min_x = 300
    max_x = 700
    min_y = 100
    max_y = 400
    dark_field = test_reconstruction[min_y:max_y, min_x:max_x, 2]
    absorption = test_reconstruction[min_y:max_y, min_x:max_x, 0]
    test_dataset = np.log(dark_field) / np.log(absorption)
    limits = stats.mstats.mquantiles(test_dataset, prob=[0.4, 0.9])
    print(limits)
    plt.tight_layout()
    im = ax.imshow(
        test_dataset,
        interpolation="none",
        clim=limits)
    cbar = figure.colorbar(im, ax=ax)

    def update_img(input_file):
        h5file = h5py.File(input_file)
        reconstruction = h5file["postprocessing/dpc_reconstruction"][...]
        dark_field = reconstruction[min_y:max_y, min_x:max_x, 2]
        absorption = reconstruction[min_y:max_y, min_x:max_x, 0]
        dataset = np.log(dark_field) / np.log(absorption)
        im.set_data(dataset)

    ani = manimation.FuncAnimation(
        figure,
        update_img,
        tqdm(input_files),
        interval=100)

    dpi=100
    writer = manimation.writers["avconv"](fps=10)
    ani.save("writer_test.mp4", writer=writer, dpi=dpi)
        

if __name__ == "__main__":
    main()
