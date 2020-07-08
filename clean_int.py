import glob, os
import pandas as pd
from datetime import datetime
import math
import dateutil.relativedelta

full_df = pd.DataFrame(columns = ['time','country', 'commodity', 'price'])
com_df = pd.DataFrame(columns = ['country', 'commodity', 'post_covid', 'yearly'])
n_r = 0
dec_19 = datetime.strptime('Dec-19', '%b-%y')
for file in glob.glob("*.csv"):
    with open(file, mode='r') as myfile:
        df = pd.read_csv(myfile, encoding='utf-8', delimiter=',')
        for c in range(1, df.shape[1]):
            year_ago = datetime.strptime('Jun-19', '%b-%y')
            end = False
            start = False
            year_ago_found = False
            text = df.columns[c]
            _, _, country, commodity, _ = text.split(", ")
            for r in range(df.shape[0]):
                month = df.iloc[r, 0]
                if len(month) == 6:
                    try:
                        formatted = datetime.strptime(month, '%y-%b')
                    except:
                        break
                else:
                    if len(month) == 8:
                        month = '0' + month
                    try:
                        formatted = datetime.strptime(month, '%d-%b-%y')
                    except:
                        break

                full_df.loc[n_r] = [formatted, country, commodity, df.iloc[r, c]]

                try:
                    ent = float(df.iloc[r, c])
                except:
                    ent = float(df.iloc[r, c].replace(',',''))

                if (end == False) & (formatted > dec_19) & (not math.isnan(ent)):
                    end = True
                    year_ago = formatted-dateutil.relativedelta.relativedelta(years=1)
                    end_p = ent

                if (start == False) & (formatted <= dec_19) & (not math.isnan(ent)):
                    start = True
                    start_p = ent

                if (year_ago_found == False) & (formatted <= year_ago):
                    year_ago_p = ent
                    year_ago_found = True
                    com_df = pd.concat(
                        [com_df,
                         pd.DataFrame([[country, commodity, (end_p - start_p) / start_p, (end_p - year_ago_p) / year_ago_p]],
                                      columns=['country', 'commodity', 'post_covid', 'yearly'])],
                        ignore_index=True)

                n_r += 1

full_df.to_csv('clean_data.csv')
com_df.to_csv('change_percent.csv')