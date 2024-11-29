import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import warnings
import numpy as np


class TestVerts:


    def test_integration(self):

        ds1 = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds1.subset(variable = "t_an")
        ds1.vertical_integration(depth_range = [0, 2.0], fixed = True)
        ds2 = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds2.subset(variable = "t_an")
        ds2.top()
        ds1.divide(ds2)
        ds1.spatial_mean()
        assert ds1.to_dataframe().t_an.values[0] == 2.0

        ff = "data/vertical_tester.nc"

        ff = "data/vertical_tester.nc"

        ds = nc.open_data(ff, checks = False)


        with pytest.raises(TypeError):
            ds.vertical_integration("e3t", depth_range = 1, fixed = True)

        with pytest.raises(ValueError):
            ds.vertical_integration("e3t", depth_range = [1,2,3], fixed = True)

        with pytest.raises(ValueError):
            ds.vertical_integration("e3t", depth_range = [30,20], fixed = True)

        with pytest.raises(TypeError):
            ds.vertical_mean("e3t", depth_range = 1)

        with pytest.raises(ValueError):
            ds.vertical_mean("e3t", depth_range = [1,2,3])

        with pytest.raises(ValueError):
            ds.vertical_mean("e3t", depth_range = [30,20])

        with pytest.raises(ValueError):
            ds.vertical_mean(thickness = 1, fixed = False)

        with pytest.raises(ValueError):
            ds.vertical_integration(thickness = 1, fixed = False)

        with pytest.raises(ValueError):
            ds.vertical_integration(thickness = ff, fixed = False)

        with pytest.raises(ValueError):
            ds.vertical_mean(thickness = ff, fixed = False)

        with pytest.raises(ValueError):
            ds1 = nc.open_data(ff, checks = False)
            ds.vertical_mean(thickness = ds1, fixed = False)

        with pytest.raises(ValueError):
            ds1 = nc.open_data(ff, checks = False)
            ds.vertical_integration(thickness = ds1, fixed = False)

        ds = nc.open_data("data/vertical_tester.nc", checks = False)
        ds.vertical_mean("e3t", depth_range = [0, 30])
        ds.spatial_sum()
        x = ds.to_dataframe().one.sum()

        ds = nc.open_data("data/vertical_tester.nc", checks = False)
        ds1 = nc.open_data("data/vertical_tester.nc", checks=False)
        ds1.subset(variables = "e3t")
        ds.vertical_mean(ds1, depth_range = [0,30])
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y


        ds = nc.open_data("data/vertical_tester.nc", checks = False)
        ds.vertical_mean("e3t")
        ds.spatial_sum()
        x = ds.to_dataframe().one.sum()

        ds = nc.open_data("data/vertical_tester.nc", checks = False)
        ds1 = nc.open_data("data/vertical_tester.nc", checks=False)
        ds1.subset(variables = "e3t")
        ds.vertical_mean(ds1)
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y

        ds = nc.open_data("data/vertical_tester.nc", checks = False)
        ds1 = nc.open_data("data/vertical_tester.nc", checks=False)
        ds1.subset(variables = "e3t")
        ds1.run()
        ds.vertical_mean(ds1[0])
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y

        version = nc.utils.cdo_version()
        if nc.utils.version_below(version, "1.9.8") == False:
            ds = nc.open_data("data/vertical_tester.nc", checks = False)
            ds.vertical_integration("e3t")
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff, checks = False)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            assert ds2.to_dataframe().one.sum() == 0

            ds = nc.open_data(ff, checks = False)
            ds.vertical_integration(depth_range=[2, 302], thickness="e3t")
            ds.spatial_max()
            assert ds.to_dataframe().one[0].astype("int") == 300


            ds = nc.open_data(ff, checks = False)
            ds3 = nc.open_data(ff, checks = False)
            ds3.subset(variable = "e3t")
            ds.vertical_integration(ds3)
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff, checks = False)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            ds2.to_dataframe().one.sum() == 0

            ds = nc.open_data(ff, checks = False)
            ds3 = nc.open_data(ff, checks = False)
            ds3.subset(variable = "e3t")
            ds3.run()
            ds.vertical_integration(ds3[0])
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff, checks = False)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            ds2.to_dataframe().one.sum() == 0



    def test_mean(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_mean(fixed = True)
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.885317325592041
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_max()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 10.37883186340332
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_min()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 4.02338171005249
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_sum()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 416.1104736328125
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_range()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.35545015335083
        n = len(nc.session_files())
        assert n == 1

    def test_intez(self):
        def foo(x):
            return np.max(x) - np.min(x)
        ds = nc.open_data("data/woa18_decav_t01_01.nc")
        ds.subset(variable = "t_an")
        ds.run()
        df = ds.to_dataframe(drop_bnds = False)
        depths = df.reset_index().loc[:,["depth", "bnds", "depth_bnds"]].drop_duplicates().drop(columns = "bnds").groupby(["depth"]).apply(foo).drop(columns = "depth").reset_index()
        depths.columns = ["depth", "depth_bnds"]
        df_check = (
        df
            .reset_index()
            .loc[:,["lon", "lat", "depth", "t_an"]]
            .drop_duplicates()
            .dropna()
            .merge(depths)
            .assign(t_an = lambda x: x.t_an * x.depth_bnds)
            .groupby(["lon", "lat"])
            .sum()
            .reset_index()
            .loc[:,["lon", "lat", "t_an"]]
        )
        ds.vertical_integration(fixed = True)
        df2 = (
        ds.to_dataframe().reset_index().dropna().loc[:,["lon", "lat", "t_an"]].rename(columns = {"t_an":"t_nc"}).merge(df_check)
        )
        assert df2.assign(check = lambda x: x.t_nc - x.t_an).check.abs().max() < 0.002
        assert float(np.corrcoef(df2.t_nc, df2.t_an)[0,1]) > 0.99

        del ds


    def test_int(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(variables="t_an")
        tracker.vertical_interp(10, fixed = True)
        x = tracker.to_dataframe().t_an.values[0].astype("float")
        n = len(nc.session_files())
        assert n == 1

    def test_surface(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff, checks = False)

        tracker.subset(variables="t_an")
        tracker.top()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        assert x == 9.660191535949707
        n = len(nc.session_files())
        assert n == 1

    def test_bottom(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff, checks = False)

        tracker.subset(variables="t_an")
        tracker.bottom()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        assert x == 4.494192123413086
        n = len(nc.session_files())
        assert n == 1

    def test_bottom_error(self):
        n = len(nc.session_files())
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff, checks = False)

        tracker.subset(variables="t_an")
        new = tracker.copy()
        new.rename({"t_an": "test"})
        new.run()
        test = nc.open_data([tracker.current[0], new.current[0]])
        # with pytest.warns(UserWarning):
        with pytest.warns(UserWarning):
            test.bottom()
            test.run()
        n = len(nc.session_files())
        assert n == 4

    def test_bottom_mask(self):
        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.subset(variables="t_an")
        df1 = data.to_dataframe().reset_index()

        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.subset(variables="t_an")
        bottom = data.copy()
        bottom.bottom_mask()
        data.multiply(bottom)
        data.vertical_max()

        df2 = (
            data.to_dataframe()
            .reset_index()
            .loc[:, ["lon", "lat", "t_an"]]
            .dropna()
            .drop_duplicates()
        )
        df2 = df2.reset_index().drop(columns="index")
        x = (
            df1.loc[:, ["lon", "lat", "depth", "t_an"]]
            .dropna()
            .drop_duplicates()
            # .rename(columns = {"t_an":"t_an2"})
            .groupby(["lon", "lat"])
            .tail(1)
            .reset_index()
            .drop(columns=["index", "depth"])
            .sort_values(["lon", "lat"])
            .reset_index()
            .drop(columns="index")
            .equals(df2.sort_values(["lon", "lat"]).reset_index().drop(columns="index"))
        )
        assert x

    def test_bottom_mask_error(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))

        with pytest.raises(TypeError):
            data.bottom_mask()

        with pytest.raises(ValueError):
            data.vertical_interp(fixed = True)

        with pytest.raises(TypeError):
            data.vertical_interp(["x"], fixed = True)

    def test_bottom_mask_error2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))

        with pytest.raises(ValueError):
            data.merge("time")
            data.bottom_mask()

        ds = nc.open_data("data/pml_ersem_nitrate_example.nc")
        ds.vertical_mean(thickness="e3t")
        ds1 = nc.open_data("data/pml_ersem_nitrate_example.nc")
        df = ds1.to_dataframe().reset_index().loc[:,["nav_lon", "nav_lat", "N3_n", "e3t"]].drop_duplicates().dropna()
        df = df.assign(N3_n = lambda x: x.N3_n * x.e3t).groupby(["nav_lon", "nav_lat"]).sum().reset_index().assign(ind = lambda x: x.N3_n / x.e3t).drop(columns = ["N3_n", "e3t"])
        df2 = ds.to_dataframe().reset_index().dropna().loc[:,["nav_lon", "nav_lat", "N3_n"]].drop_duplicates().merge(df)
        assert df2.assign(check = lambda x: x.N3_n - x.ind).check.abs().max() < 0.02
        ds = nc.open_data("data/pml_ersem_nitrate_example.nc")
        df = ds.to_dataframe()
        df = df.reset_index().loc[:,["nav_lon", "nav_lat", "N3_n", "e3t", "deptht"]].dropna().drop_duplicates()
        df = df.assign(N3_n = lambda x: x.N3_n * x.e3t).groupby(["nav_lon", "nav_lat"]).sum()
        df = df.reset_index().drop(columns = "e3t").rename(columns = {"N3_n":"ind"})
        ds = nc.open_data("data/pml_ersem_nitrate_example.nc")
        ds.vertical_integration( thickness = "e3t" )
        df_match = ds.to_dataframe().reset_index().loc[:,["nav_lon", "nav_lat", "N3_n"]].dropna().drop_duplicates().merge(df)
        assert df_match.assign(check123 = lambda x: x.ind- x.N3_n).check123.abs().max() < 0.1

        del ds

    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_depth_option(self):
        ds = nc.open_data("data/pml_ersem_nitrate_example.nc")
        ds.vertical_interp(levels = [50], thickness="e3t", surface = "top")
        ds.subset(variables = "N3_n")
        ds.run()

        ds_depths = nc.open_data("data/pml_ersem_nitrate_example.nc")
        ds_depths.subset(variable="e3t")
        ds_depths.missing_as(1.0)
        ds_medium = ds_depths.copy()
        ds_medium / 2
        ds_depths.vertical_cumsum()
        ds_depths.run()
        ds_depths - ds_medium
        ds_depths.run()

        ds1 = nc.open_data("data/pml_ersem_nitrate_example.nc")
        ds1.subset(variable="N3_n")
        ds1.vertical_interp(levels = [50], depths= ds_depths, fixed = False)
        ds1.run()

        ds2 = ds1.copy()
        ds2 - ds
        ds2.abs()
        ds2.run()

        assert ds2.to_dataframe().N3_n.max() < 0.000001

