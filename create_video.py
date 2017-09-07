import click
import numpy as np
import h5py
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from matplotlib import ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
from matplotlib.patches import Rectangle


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
        figure, (ax, ratio_ax) = plt.subplots(1, 2)
        plt.subplots_adjust(
            wspace=0.02,
            hspace=0.02)
        plt.subplots_adjust(top=0.8)
        dataset_names = list(input_h5_file.keys())
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
        ax.tick_params(
            axis='both', which='both', bottom='off', top='off',
            labelbottom='off', right='off', left='off',
            labelleft='off')
        ax.add_patch(Rectangle((37, 13), 30, 5, facecolor="red"))
        ax.text(52, 23, "1 mm", ha="center", va="top", color="red")
        ax.set_frame_on(False)
        ratio_ax.set_frame_on(False)
        ratio_ax.tick_params(
            axis='both', which='both', bottom='off', top='off',
            labelbottom='off', right='off', left='off',
            labelleft='off')
        abs_divider = make_axes_locatable(ax)
        abs_cax = abs_divider.append_axes(
            "left", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=abs_cax)
        cbar.ax.yaxis.set_ticks_position("left")
        abs_tick_locator = ticker.MaxNLocator(nbins=4)
        cbar.locator = abs_tick_locator
        cbar.update_ticks()
        ax.set_title(r"$-\log(\mathrm{transmission})$")
        ratio_ax.set_title(
            r"$\frac{\log(\mathrm{vis\, reduction})}{\log(\mathrm{transmission})}$")
        ratio_im = ratio_ax.imshow(
            ratio_dataset,
            interpolation="none",
            clim=limits[2])
        ratio_divider = make_axes_locatable(ratio_ax)
        ratio_cax = ratio_divider.append_axes(
            "right", size="5%", pad=0.05)
        ratio_colorbar = plt.colorbar(ratio_im, cax=ratio_cax)
        ratio_tick_locator = ticker.MaxNLocator(nbins=4)
        ratio_colorbar.locator = ratio_tick_locator
        ratio_colorbar.update_ticks()

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
