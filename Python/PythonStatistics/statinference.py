import pandas as pd
import numpy as np
import kagglehub
import os
from scipy import stats

# Download latest version
path = kagglehub.dataset_download("anshtanwar/metro-interstate-traffic-volume")

print("Path to dataset files:", path)
csv_file = None
for file in os.listdir(path):
    if file.endswith('.csv'):
        csv_file = os.path.join(path, file)
        break

if csv_file is None:
    print("No CSV file found in the directory.")
else:
    print(f"Found CSV file: {csv_file}")
    # Read the CSV file
    #Population Data
    df = pd.read_csv(csv_file, delimiter=',')
    print(df.head())
    print(f'shape of a dataset: {df.shape}')
    mean_traffic_volume = df['traffic_volume'].mean()
    print(f'population mean(avg traffic volume) : {mean_traffic_volume}')

    # Sample Data
    l=[10,20,30,40,50]
    p=[]
    m=[]
    n=1
    for i in l:
        sampled_df = df.sample(n=1000, random_state=i)
        #print(f'shape of a dataset: {sampled_df.shape}')
        print(f'************Sample {n}******************')
        n=n+1
        sample_mean_traffic_volume = sampled_df['traffic_volume'].mean()
        print(f'sample mean(point of estimate for the average traffic volume of population) : {sample_mean_traffic_volume}')


        #Null Hypothesis(n_0) -> sample mean = population mean
        #Alternate Hypothesis(n_1) -> sample mean!= population mean

        t_statistic, p_value = stats.ttest_1samp(sampled_df['traffic_volume'], mean_traffic_volume)
        m.append(round(sample_mean_traffic_volume,2))
        p.append(round(p_value,2))
        print(f"T-statistic: {t_statistic}")
        print(f"P-value: {p_value}")

        #significance valu
        alpha = 0.05
        if(p_value<0.05):
            print("Reject the Null Hypothesis. Sample mean is different from the population mean")
        else:
            print("Fail to reject the Null Hypothesis: sample mean is approximately equal to the population mean")
    samples=dict(zip(m,p))
    print(samples)
    


