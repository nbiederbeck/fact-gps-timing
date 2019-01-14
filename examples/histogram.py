from astropy.table import Table
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt


def read_with_row_mask(dataset, mask):
    rows, columns = dataset.shape
    mask_2d = np.repeat(mask, columns).reshape((rows, columns))
    return dataset[mask_2d].reshape((mask.sum(), columns))


def plot_histogram():
    fits_file = fits.open(
        "/data/fact/gps_timestamp_data/2013/11/26/20131126_127_v1.1.1_gps_timestamp_data_timestamps.fits"
    )
    table = Table(fits_file[1].data)
    gps_triggers = table["TriggerType"] == 1

    unix_time_utc = read_with_row_mask(table["UnixTimeUTC"], gps_triggers).astype(
        "uint64"
    )
    timestamp = np.array(
        unix_time_utc[:, 0] * 1_000_000 + unix_time_utc[:, 1], dtype="datetime64[us]"
    )
    full_second = (timestamp + np.timedelta64(500, "ms")).astype("datetime64[s]")

    fig, ax = plt.subplots()
    ax.hist(np.abs(timestamp - full_second).astype(int) / 1000, bins=100)
    ax.set_xlabel("Absolute time difference to full UTC second in ms")
    fig.tight_layout()
    fig.savefig("build/histogram.pdf")


if __name__ == "__main__":
    plot_histogram()
