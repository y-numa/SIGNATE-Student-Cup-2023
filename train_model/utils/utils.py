import pandas as pd
import math
from geopy.geocoders import Nominatim
import numpy as np
from tqdm import tqdm



def create_geo_feat(geo_df):
    cal_geo_list = pd.concat([geo_df['region_ver1'], geo_df['region_ver2'], geo_df['region_ver3']])

    cal_geo_list = list(set(cal_geo_list[~cal_geo_list.isna()]))

    geo_dict_df = pd.DataFrame(cal_geo_list)
    geo_dict_df.columns = ['region']

    geo_dict_df['region_long'] = np.nan
    geo_dict_df['region_lat'] = np.nan

    geo = Nominatim(user_agent="myapp", timeout=10)

    for loop_num in tqdm(range(geo_dict_df.shape[0])):
        location = geo.geocode(geo_dict_df['region'].iat[loop_num])
        try:
            geo_dict_df['region_lat'].iat[loop_num] = location.latitude
            geo_dict_df['region_long'].iat[loop_num] = location.longitude
        except AttributeError:
            geo_dict_df['region_lat'].iat[loop_num] = np.nan
            geo_dict_df['region_long'].iat[loop_num] = np.nan

    output_geo_df = pd.DataFrame()

    tmp_df = pd.merge(geo_df['region_ver1'], geo_dict_df.rename({'region':'region_ver1'},axis=1), how='left', on='region_ver1')
    tmp_df.columns = ['region_ver1', 'region_long', 'region_lat']

    output_geo_df = pd.concat([output_geo_df, tmp_df[['region_long', 'region_lat']]], axis=1)

    tmp_df = pd.merge(geo_df['region_ver2'], geo_dict_df.rename({'region':'region_ver2'},axis=1), how='left', on='region_ver2')
    tmp_df.columns = ['region_ver2', 'region_ver2_long', 'region_ver2_lat']

    output_geo_df = pd.concat([output_geo_df, tmp_df[['region_ver2_long', 'region_ver2_lat']]], axis=1)

    tmp_df = pd.merge(geo_df['region_ver3'], geo_dict_df.rename({'region':'region_ver3'},axis=1), how='left', on='region_ver3')
    tmp_df.columns = ['region_ver3', 'region_ver3_long', 'region_ver3_lat']

    output_geo_df = pd.concat([output_geo_df, tmp_df[['region_ver3_long', 'region_ver3_lat']]], axis=1)

    for loop_num in tqdm(range(output_geo_df.shape[0])):
        if not math.isnan(output_geo_df['region_ver2_long'].iat[loop_num]): 
            if not math.isnan(output_geo_df['region_ver3_long'].iat[loop_num]): 
                output_geo_df['region_long'].iat[loop_num] = (output_geo_df['region_long'].iat[loop_num] + output_geo_df['region_ver2_long'].iat[loop_num]+ output_geo_df['region_ver3_long'].iat[loop_num])/3
                output_geo_df['region_lat'].iat[loop_num] = (output_geo_df['region_lat'].iat[loop_num] + output_geo_df['region_ver2_lat'].iat[loop_num]+ output_geo_df['region_ver3_lat'].iat[loop_num])/3
            else:
                output_geo_df['region_long'].iat[loop_num] = (output_geo_df['region_long'].iat[loop_num] + output_geo_df['region_ver2_long'].iat[loop_num])/2
                output_geo_df['region_lat'].iat[loop_num] = (output_geo_df['region_lat'].iat[loop_num] + output_geo_df['region_ver2_lat'].iat[loop_num])/2
    return output_geo_df[['region_long', 'region_lat']]
    # return pd.concat([geo_df['id'], output_geo_df[['region_long', 'region_lat']]], axis=1)