import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import platform


class TestTonnc:
    def test_empty(self):

        ds = nc.open_data("data/sst.mon.mean.nc", checks = False)
        times = ds.times
        out = nc.temp_file.temp_file("nc")
        nc.session.append_safe(out)
        ds.to_nc(out, time = 1)
        ds = nc.open_data(out, checks = False)
        assert  len(ds.times) == 1
        assert ds.times[0] == times[1]
        nc.session.remove_safe(out)
        del ds


        ds = nc.open_data("data/sst.mon.mean.nc", checks = False)
        times = ds.times
        out = nc.temp_file.temp_file("nc")
        nc.session.append_safe(out)
        ds.to_nc(out, time = 1, zip = False)
        ds = nc.open_data(out, checks = False)
        assert  len(ds.times) == 1
        assert ds.times[0] == times[1]
        nc.session.remove_safe(out)
        del ds
        n = len(nc.session_files())
        assert n == 0
        ds = nc.open_data()
        with pytest.raises(ValueError):
            ds.to_nc("/tmp/test.nc")

        out_file = "test123.nc"
        ds = nc.open_data(["data/2003.nc", "data/2004.nc"], checks = False)
        ds.subset(time = 0)
        ds.merge("time")
        ds.to_nc(out_file, overwrite=True)
        os.path.exists(out_file)
        ds = nc.open_data(["data/2003.nc", "data/2004.nc"], checks = False)
        ds.subset(time = 0)
        ds.merge("time")
        ds.to_nc(out_file, overwrite=True)
        os.remove(out_file)

    def test_1(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.to_nc(ff1)
        data1 = nc.open_data(ff1, checks=False)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        assert x == y

    def test_2(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.run()
        data.to_nc(ff1, zip=False)
        data1 = nc.open_data(ff1, checks=False)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        assert x == y

        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.to_nc(ff1, zip=False)
        data1 = nc.open_data(ff1, checks=False)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        assert x == y



    def test_3(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.run()
        data.to_nc(ff1, zip=False)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.run()
        data.to_nc(ff1, zip=True)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)
        assert x == y

    def test_4(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.to_nc(ff1, zip=False)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.to_nc(ff1, zip=True)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        assert x == y

    def test_5(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=[0, 1])
        data.tmean()
        data.to_nc(ff1, zip=False)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        ff = "data/sst.mon.mean.nc"
        ff1 = nc.temp_file.temp_file(".nc")
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=[0, 1])
        data.split("yearmonth")
        data.ensemble_mean()
        data.to_nc(ff1, zip=True)

        data1 = nc.open_data(ff1, checks=False)
        data1.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)

        assert x == y

    def test_ens(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=[0, 1, 2])
        data.split("yearmonth")
        with pytest.raises(ValueError):
            data.to_nc("/tmp/test.nc")

        with pytest.raises(ValueError):
            data.to_nc("/tmp/asdfu1nuuu2/test.nc")




    def test_overwrite(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            data.to_nc(ff)

    def test_osx(self):
        # only run on non-linux
        if platform.system() != "Linux":
            ff = "data/sst.mon.mean.nc"

            ds = nc.open_data(ff, checks = False)
            ds.subset(timesteps= 0)
            ds.to_nc("~/Downloads/test.nc")

            ds1 = nc.open_data("~/Downloads/test.nc", checks = False)

            ds1 - ds

            # make sure everything is zero in ds1

            ds1.spatial_mean()

            assert ds1.to_dataframe().sst.values[0] == 0


