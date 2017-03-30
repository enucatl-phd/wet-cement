import h5py
import numpy as np
from scipy import stats
import click
import matplotlib.pyplot as plt
import os
from tqdm import tqdm


@click.command()
@click.argument(
    "file_names",
    nargs=-1,
    type=click.Path(exists=True)
)
@click.option("--output")
def main(file_names, output):
    min_x = 50
    max_x = 400
    min_y = 450
    max_y = 650
    column_gaps = np.array(
        [254, 255, 256, 257, 513, 514, 515, 516, 770, 771, 772, 773],
        dtype=np.int)
    row_gaps = np.array([253, 254, 255, 256, 257, 258])
    with h5py.File(output, "w") as outh5file:
        for file_name in tqdm(file_names):
            with h5py.File(file_name, "r") as h5file:
                original_dataset = h5file["postprocessing/dpc_reconstruction"]
                masked = np.delete(
                    original_dataset,
                    row_gaps,
                    axis=0)
                masked = np.delete(
                    masked,
                    column_gaps,
                    axis=1)
                cropped = masked[min_x:max_x, min_y:max_y, ...]
                dataset = np.zeros(cropped.shape)
                dataset[..., 0] = -np.log(cropped[..., 0])
                dataset[..., 1] = -np.log(cropped[..., 2])
                dataset[..., 2] = dataset[..., 1] / dataset[..., 0]
                timestamp = os.path.basename(file_name).split("_")[0]
                outh5file[timestamp] = dataset
                # plt.figure()
                # plt.imshow(
                    # dataset[..., 2],
                    # clim=(0.5,2.5),
                    # interpolation="none"
                # )
                # plt.ion()
                # plt.show()
                # input()
                # break


if __name__ == "__main__":
    main()
