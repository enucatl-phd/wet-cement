import h5py
import subprocess
import os
from tqdm import tqdm

def main():
    data = open("datasets.csv").readlines()
    flat = "/sls/X02DA/data/e14980/Data10/disk2/High_Energy_Setup/TITLIS_DATA/2017_03_27/170327.115258642953.h5"
    print(flat)
    print(data)
    for d in tqdm(data):
        subprocess.check_call(
            "dpc_radiography\
            --overwrite\
            --group /entry/data/th_0\
            --drop_last {0} {1}\
            ".format(d.strip(), flat),
            cwd="../dpc_reconstruction",
            shell=True,
        )


if __name__ == "__main__":
    main()
