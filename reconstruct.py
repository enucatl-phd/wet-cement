import h5py
import subprocess
import os
from tqdm import tqdm

def main():
    input_list = [
        os.path.abspath(os.path.join("data", os.path.basename(f)).strip())
        for f in open("datasets.csv").readlines()]
    flats = [input_list[0]] + input_list[-9:]
    data = input_list[1:-10]
    print(flats)
    print(data)
    for d in tqdm(data):
        subprocess.check_call(
            "dpc_radiography\
            --group /entry/data\
            --drop_last {0} {1}\
            ".format(d, flats[0]),
            cwd="../dpc_reconstruction",
            shell=True,
        )


if __name__ == "__main__":
    main()
