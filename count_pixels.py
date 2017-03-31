import click
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import csv
import h5py
import datetime


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file")
def main(input_file, output_file):
    with h5py.File(input_file, "r") as input_h5_file:
        with open(output_file, "w") as output_csv_file:
            writer = csv.writer(output_csv_file)
            writer.writerow(["time", "wet_fraction", "wet_pixels"])
            for dataset_name in tqdm(input_h5_file):
                dataset = input_h5_file[dataset_name][...]
                # plt.figure()
                # plt.hist(
                    # dataset,
                    # bins=50,
                    # range=(0.5, 2.5),
                # )
                # plt.ion()
                # plt.show()
                # input()
                # break
                threshold = 1.18
                wet_pixels = np.size(dataset[dataset < threshold])
                wet_fraction = (
                    np.size(dataset[dataset < threshold]) /
                    np.size(dataset))
                time = datetime.datetime.strptime(
                    dataset_name, "%y%m%d.%H%M%S%f")
                writer.writerow([
                    int(time.strftime("%s")),
                    wet_fraction,
                    wet_pixels])


if __name__ == "__main__":
    main()
