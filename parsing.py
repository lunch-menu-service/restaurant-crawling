import time

from tqdm import tqdm
import pandas as pd
from pyproj import Proj, transform

# parse dataset
df = pd.read_csv('dataset/fulldata_07_24_04_P.csv', encoding='cp949')

# filter the closed/banned restaurant
df = df[df['영업상태구분코드'] == 1]

# filter the restaurant which has no position data
df = df.dropna(subset=['좌표정보(x)', '좌표정보(y)'])

# convert position data from EPSG:5174 to EPSG:4326
proj_src = Proj(init='epsg:5174')
proj_dst = Proj(init='epsg:4326')
dst_positions = transform(proj_src, proj_dst, df['좌표정보(x)'].values, df['좌표정보(y)'].values)
df['X'] = dst_positions[0]
df['Y'] = dst_positions[1]

# filter the restaurant which has no information in Naver Map API
from naver_map import is_available_restaurant
availables = []
print(len(df))
with tqdm(total=len(df)) as pbar:
    for query, x, y in tqdm(zip(df['사업장명'].values, df['X'].values, df['Y'].values)):
        try:
            availables.append(is_available_restaurant(query=query, x=float(x), y=float(y)))
            #time.sleep(0.5)
            pbar.update(1)
        except Exception as e:
            print(e)

df['available'] = availables
df = df[df['available'] == True]

# filter useless columns
df = df[['사업장명', 'X', 'Y', '최종수정시점']]

# look dataframe
print(df)
