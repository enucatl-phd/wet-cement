import click
import numpy as np
import h5py
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        with h5py.File(output_file, "w") as output_h5_file:
            for dataset_name in tqdm(input_h5_file):
                dataset = input_h5_file[dataset_name]
                filtered = np.zeros_like(dataset)
                absorption = dataset[..., 0]
                dark_field = dataset[..., 1]
                ratio = dataset[..., 2]
                f = filters.median_filter
                s = 3
                filtered[..., 0] = f(absorption, s)
                filtered[..., 1] = f(dark_field, s)
                filtered[..., 2] = f(ratio, s)
                # plt.figure()
                # plt.imshow(
                    # filtered[..., 2],
                    # clim=(0.5,2.5),
                    # interpolation="none"
                # )
                # plt.ion()
                # plt.show()
                # input()
                # break
                output_h5_file[dataset_name] = filtered


if __name__ == "__main__":
    main()
