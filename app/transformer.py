import dask.dataframe as dd
import pandas as pd
from tabulate import tabulate

from dask.distributed import Client, wait

class ErrorTransformer(BaseException):
    def __init__(self, message):
        self.message = message

class Transformer:
    def __init__(self, logger, client=None):
        """
        Init function: client as optional
        This is used for code reusability for local run and distributed run.
        """
        self.logger = logger

        self.logger.info(f' Creating Transformer {client=}')
        self.client = client

    def distribute_data(self, publishers_df, ads_df):
        """
        Function: Scatter data across cluster in distributed runtime.
        But in actual production run, using a shared storage would
        be much faster instead of scattering.
        """
        
        self.logger.info('Starting to distribute data')
        publishers_future = self.client.scatter(publishers_df)
        ads_future = self.client.scatter(ads_df)
        
        wait([publishers_future, ads_future])
        
        publishers_ddf = dd.from_pandas(publishers_future.result(),
                                        npartitions=2)
        ads_ddf = dd.from_pandas(ads_future.result(),
                                 npartitions=2)
        
        return publishers_ddf, ads_ddf

        
    def transform_data(self, pub_path, ads_path, date, out_path=None):
        """
        Function: Data Ingestion part, used to convert to Dask DataFrame based on the run type.
        """
        publishers_df = pd.read_csv(pub_path)
        ads_df = pd.read_csv(ads_path)
        self.logger.info(f'New Job : {ads_df.count()}, {publishers_df.count()}')
        
        if self.client:
            pub_ddf, ads_ddf = self.distribute_data(publishers_df, ads_df)
        else:
            pub_ddf = dd.from_pandas(publishers_df,
                                        npartitions=2)
            ads_ddf = dd.from_pandas(ads_df,
                                        npartitions=2)

        return self.calculate_sum(pub_ddf, ads_ddf, date, out_path)

    
    def calculate_sum(self, pub_ddf, ads_ddf, date, out_path=None):
        """
        Function: Transformation Part.
        """
        self.logger.info('calculating result')
        ads_ddf = ads_ddf[ads_ddf['DATE'] == date]
        publisher_names = pub_ddf.set_index('ID')['NAME'].compute().to_dict()

        daily_revenue = ads_ddf.groupby(['DATE', 'PUBLISHER_ID'])['REVENUE'].sum().reset_index()
        daily_revenue['PUBLISHER_NAME'] = daily_revenue['PUBLISHER_ID'].map(publisher_names, meta=('PUBLISHER_ID', 'object'))
        result = daily_revenue[['DATE', 'PUBLISHER_NAME', 'REVENUE']].compute()

        self.logger.info(f'Writing to file {out_path}')
        result.to_csv(out_path)
        self.logger.info(f'Printing result')
        print(tabulate(result, headers='keys', tablefmt='psql'))
        return result

    
