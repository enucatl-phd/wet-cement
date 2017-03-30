import click
import numpy as np
import h5py
import scipy.ndimage.filters as filters


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        with h5py.File(output_file, "w") as output_h5_file:
            for dataset_name in input_h5_file:
                print(dataset_name)


if __name__ == "__main__":
    main()
