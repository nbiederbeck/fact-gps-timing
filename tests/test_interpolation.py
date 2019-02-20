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

def main():
    path = '/net/big-tank/POOL/projects/fact/gps_timestamp_data/2014/01/01/20140101_073_v1.1.1_gps_timestamp_data_timestamps.fits'
    test_time_differences_greater_zero(path)

if __name__ == "__main__":
    main()
