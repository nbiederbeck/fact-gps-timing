from astropy.table import Table
import numpy as np
from .exceptions import NoGPSTriggers


def interpolate_boardtimes(table: Table, trigger_gps_value: int = 1):
    """Interpolate boardtimes with GPS triggers.

    Read UnixTimeUTC and BoardTime as unsigned integers,
    reduce the timestamps to full seconds,
    and zero-correct the boardtimes.
    Run a linear regression on the GPS triggered timestamps,
    to interpolate the boardtimes.
    Add the interpolated boardtimes to the table and return it.

    Avoid BoardCounter integer overflow problems by subtracting
    the first element and thus re-underflowing the problematic
    values which solves this problem easily.

    Parameters
    ----------
    table: astropy.table.Table

    Returns
    -------
    astropy.table.Table
    """
    # Get mask where event was triggered by GPS
    gps_triggers_mask = table["TriggerType"] == trigger_gps_value
    if np.sum(gps_triggers_mask) == 0:
        raise NoGPSTriggers

    # Read UnixTimeUTC and BoardTime as 32bit unsigned integers
    unixtimeutc = table["UnixTimeUTC"].astype("uint32")
    timestamps = np.array(
        unixtimeutc[:, 0] * 1e6 + unixtimeutc[:, 1], dtype="datetime64[us]"
    )
    full_seconds = (timestamps + np.timedelta64(500, "ms")).astype("datetime64[s]")
    full_seconds_int = full_seconds.astype("uint32")
    boardtimes = table["BoardTime"].astype("uint32")

    # Zero-correct board times (start at 0 for first event)
    boardtimes_corr = boardtimes - boardtimes[0, :]

    # Calculate mean boardtimes from 40 counters
    mean_boardtimes_corr = boardtimes_corr.mean(axis=1)

    # Linear interpolation (y = x * m + b)
    m, b = np.polyfit(
        mean_boardtimes_corr[gps_triggers_mask],
        full_seconds_int[gps_triggers_mask],
        deg=1,
    )

    # Add new column to data table and return it
    table["InterpolatedUnixTime"] = mean_boardtimes_corr * m + b

    return table
