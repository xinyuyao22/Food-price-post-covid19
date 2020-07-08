import glob, os
import pandas as pd
from datetime import datetime
import math
import dateutil.relativedelta

full_df = pd.DataFrame(columns = ['month','country', 'price_type', 'market', 'commodity', 'price'])
com_df = pd.DataFrame(columns = ['country', 'price_type', 'market', 'commodity', 'percent'])
n_r = 0
nov_19 = datetime.strptime('Nov-19', '%b-%y')
for file in glob.glob("*.csv"):
    with open(file, mode='r') as myfile:
        df = pd.read_csv(myfile, encoding='utf-8', delimiter=',')
        for c in range(1, df.shape[1]):
            year_ago = 0
            end = False
            start = False
            text = df.columns[c]
            country, price_type, market, commodity, _ = text.split(", ")
            for r in range(df.shape[0]):
                month = df.iloc[r, 0]
                try:
                    formatted = datetime.strptime(month, '%b-%y')
                except:
                    try:
                        formatted = datetime.strptime(month, '%y-%b')
                    except:
                        break

                full_df.loc[n_r] = [formatted, country, price_type, market, commodity, df.iloc[r, c]]

                if (end == False) & (formatted > nov_19) & (not math.isnan(float(df.iloc[r, c]))):
                    end = True
                    year_ago = formatted-dateutil.relativedelta.relativedelta(years=1)
                    end_p = float(df.iloc[r, c])

                if (start == False) & (formatted == nov_19) & (not math.isnan(float(df.iloc[r, c]))):
                    start = True
                    start_p = float(df.iloc[r, c])

                if (formatted == year_ago):
                    year_ago_p = float(df.iloc[r, c])
                    com_df = pd.concat(
                        [com_df,
                         pd.DataFrame([[country, price_type, market, commodity, (end_p - start_p) / start_p * 100, (end_p - year_ago_p) / year_ago_p * 100]],
                                      columns=['country', 'price_type', 'market', 'commodity', 'post_covid', 'yearly'])],
                        ignore_index=True)

                n_r += 1

full_df.to_csv('clean_data.csv')
com_df.to_csv('change_percent.csv')