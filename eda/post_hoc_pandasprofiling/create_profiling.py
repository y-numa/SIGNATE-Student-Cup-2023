import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_pickle('../../preprocessing/preprocess_df.pkl')
profile = ProfileReport(df) 
profile.to_file(output_file='report.html')