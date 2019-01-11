from astropy.table import Table
from scipy.optimize import curve_fit
import numpy as np


def interpolate_boardtimes(table: Table):
    """Interpolate boardtimes with GPS triggers.

    Read UnixTimeUTC and BoardTime as unsigned integers,
    reduce the timestamps to full seconds,
    and zero-correct the boardtimes.
    Run a linear regression on the GPS triggered timestamps,
    to interpolate the boardtimes.
    Add the interpolated boardtimes to the table and return it.

    Parameters
    ----------
    table: astropy.table.Table

    Returns
    -------
    astropy.table.Table
    """
    # Read UnixTimeUTC and BoardTime as 32bit and 63bit unsigned integers
    unixtimeutc = table["UnixTimeUTC"].astype("uint32")
    timestamps = np.array(
        unixtimeutc[:, 0] * 1e6 + unixtimeutc[:, 1], dtype="datetime64[us]"
    )
    full_seconds = (timestamps + np.timedelta64(500, "ms")).astype("datetime64[s]")
    full_seconds_int = full_seconds.astype("uint32")
    boardtimes = table["BoardTime"].astype("uint64")

    # Zero-correct board times (start at 0 for first event)
    boardtimes_corr = boardtimes - boardtimes[0, :]

    # Calculate mean boardtimes from 40 counters
    mean_boardtimes_corr = boardtimes_corr.mean(axis=1)

    # Get mask where event was triggered by GPS
    gps_triggers_mask = table["TriggerType"] == 1

    # Define and fit linear function
    def _linear_interpolation(x, m, b):
        return x * m + b

    par, cov = curve_fit(
        _linear_interpolation,
        mean_boardtimes_corr[gps_triggers_mask],
        full_seconds_int[gps_triggers_mask],
    )

    # Add new column to data table and return it
    table["InterpolatedUnixTime"] = _linear_interpolation(mean_boardtimes_corr, *par)

    return table
