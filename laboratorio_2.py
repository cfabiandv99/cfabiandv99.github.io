# -*- coding: utf-8 -*-
"""1 PPvsSpark_01.ipynb

# Pandas vs Polars vs Spark vs Dask
SEMINARIO DE BIG DATA
    Laboratorio No. 2
    Presentado por: Carlos Fabian Diaz Vargas
    Codigo estudiantil: 90368
    Programa: Ingenieria de sistemas
"""

from google.colab import drive
drive.mount('/content/drive')

"""## Playing with pandas"""

import pandas as pd
# flights_file1 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2018.parquet"
#flights_file2 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2019.parquet"
flights_file3 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2020.parquet"
flights_file4 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2021.parquet"
#flights_file5 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2022.parquet"
# df1 = pd.read_parquet(flights_file1)
#df2 = pd.read_parquet(flights_file2)
df3 = pd.read_parquet(flights_file3)
df4 = pd.read_parquet(flights_file4)
#df5 = pd.read_parquet(flights_file5)

df = pd.concat([df3, df4])
# df = df2

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# 
# df_agg = df.groupby(['Airline','Year'])[["DepDelayMinutes", "ArrDelayMinutes"]].agg(
#     ["mean", "sum", "max"]
# )
# df_agg = df_agg.reset_index()
# df_agg.to_parquet("temp_pandas.parquet")

!ls -GFlash temp_pandas.parquet

pd.read_parquet('temp_pandas.parquet')

pd.read_parquet('temp_pandas.parquet').info()

"""## Playing with Polars"""

import polars as pl

#flights_file1 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2018.parquet"
#flights_file2 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2019.parquet"
flights_file3 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2020.parquet"
flights_file4 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2021.parquet"
#flights_file5 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2022.parquet"
#df1 = pl.scan_parquet(flights_file1)
#df2 = pl.scan_parquet(flights_file2)
df3 = pl.scan_parquet(flights_file3)
df4 = pl.scan_parquet(flights_file4)
#df5 = pl.scan_parquet(flights_file5)

# Commented out IPython magic to ensure Python compatibility.
#  %%timeit

df_polars = (
    pl.concat([df3, df4])
    .group_by(['Airline', 'Year'])
    .agg([
        pl.col("DepDelayMinutes").mean().alias("avg_dep_delay"),
        pl.col("DepDelayMinutes").sum().alias("sum_dep_delay"),
        pl.col("DepDelayMinutes").max().alias("max_dep_delay"),
        pl.col("ArrDelayMinutes").mean().alias("avg_arr_delay"),
        pl.col("ArrDelayMinutes").sum().alias("sum_arr_delay"),
        pl.col("ArrDelayMinutes").max().alias("max_arr_delay"),
      ])
).collect()

df_polars.write_parquet('temp_polars.parquet')

!ls -GFlash temp_polars.parquet

"""## Playing with PySpark"""

!pip install pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, sum, concat

spark = SparkSession.builder.master("local[1]").appName("airline-example").getOrCreate()

#flights_file1 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2018.parquet"
#flights_file2 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2019.parquet"
flights_file3 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2020.parquet"
flights_file4 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2021.parquet"
#flights_file5 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2022.parquet"

#df_spark1 = spark.read.parquet(flights_file1)
#df_spark2 = spark.read.parquet(flights_file2)
df_spark3 = spark.read.parquet(flights_file3)
df_spark4 = spark.read.parquet(flights_file4)
#df_spark5 = spark.read.parquet(flights_file5)

#df_spark = df_spark1.union(df_spark2)
df_spark = df_spark3.union(df_spark3)
df_spark = df_spark4.union(df_spark4)
#df_spark = df_spark.union(df_spark5)

# Commented out IPython magic to ensure Python compatibility.
#  %%timeit

df_spark_agg = df_spark.groupby("Airline", "Year").agg(
    avg("ArrDelayMinutes").alias('avg_arr_delay'),
    sum("ArrDelayMinutes").alias('sum_arr_delay'),
    max("ArrDelayMinutes").alias('max_arr_delay'),
    avg("DepDelayMinutes").alias('avg_dep_delay'),
    sum("DepDelayMinutes").alias('sum_dep_delay'),
    max("DepDelayMinutes").alias('max_dep_delay'),
)
df_spark_agg.write.mode('overwrite').parquet('temp_spark.parquet')

!ls -GFlash temp_spark.parquet

"""## Playing with dask"""

import pandas as pd
import dask.dataframe as dd
# flights_file1 = "/content/drive/MyDrive/data/flights/Combined_Flights_2018.parquet"
# flights_file2 = "/content/drive/MyDrive/data/flights/Combined_Flights_2019.parquet"
flights_file3 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2020.parquet"
flights_file4 = "/content/drive/MyDrive/Seminario/bigData/flights/Combined_Flights_2021.parquet"
#flights_file5 = "/content/drive/MyDrive/data/flights/Combined_Flights_2022.parquet"
# df1 = dd.read_parquet(flights_file1)
# df2 = dd.read_parquet(flights_file2)
df3 = dd.read_parquet(flights_file3)
df4 = dd.read_parquet(flights_file4)
# df5 = dd.read_parquet(flights_file5)

df = dd.concat([df3, df4])

print(df.compute())

df = df.compute()

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# 
# df_agg = df.groupby(['Airline','Year'])[["DepDelayMinutes", "ArrDelayMinutes"]].agg(
#     ["mean", "sum", "max"]
# )
# df_agg = df_agg.reset_index()
# df_agg.to_parquet("temp_dask.parquet")

!ls -GFlash temp_pandas.parquet

pd.read_parquet('temp_dask.parquet').info()

pd.read_parquet('temp_dask.parquet')

"""## Read Results"""

import pandas as pd

agg_pandas = pd.read_parquet('temp_pandas.parquet')
agg_polars = pd.read_parquet('temp_polars.parquet')
agg_spark = pd.read_parquet('temp_spark.parquet')
agg_dask = pd.read_parquet('temp_dask.parquet')

agg_pandas.shape, agg_polars.shape, agg_spark.shape, agg_dask.shape

agg_pandas.sort_values(['Airline','Year']).head()

agg_polars.sort_values(['Airline','Year']).head()

agg_spark.sort_values(['Airline','Year']).head()

agg_dask.sort_values(['Airline','Year']).head()
