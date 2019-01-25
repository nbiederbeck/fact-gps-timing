from astropy.table import Table
from astropy.io import fits
from GPSTiming.interpolation import interpolate_boardtimes
from numpy import diff


def test_time_differences_greater_zero(path: str):
    fits_file = fits.open(path)
    table = Table(fits_file[1].data)
    fits_file.close()
    table = interpolate_boardtimes(table)
    assert diff(table["InterpolatedUnixTime"]).all() > 0
