import pandas as pd
import numpy as np
import kagglehub
import os

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
    df = pd.read_csv(csv_file, delimiter=',')
    print(df.head())

    df1 = df.groupby('weather_main')['traffic_volume'].mean().sort_values()
    print("Average Traffic Volume based on Weather main")
    print(df1)
    print("No. of data points for particular weather")
    print(df['weather_main'].value_counts())

    # prob of trafficvol>3000 given weather rain
    #A->trafficvol>3000
    #B->weather rain
    p_traffic_gt_3000 = len(df[df['traffic_volume'] > 3000]) / len(df) 
    print(f'p_traffic_gt_3000: {p_traffic_gt_3000}')
    p_rain = len(df[df['weather_main'] == 'Rain']) / len(df) 
    print(f'p_rain: {p_rain}')
    # Use boolean indexing correctly
    traffic_gt_3000_and_rain = df[(df['traffic_volume'] > 3000) & (df['weather_main'] == 'Rain')]
    p_rain_given_trafficvol_gt_3000 = len(traffic_gt_3000_and_rain) / len(df[df['traffic_volume'] > 3000])
    print(f'p_rain_given_trafficvol_gt_3000:{p_rain_given_trafficvol_gt_3000}')
    #Bayes Theorm
    p_trafficvol_gt_3000_given_rain = (p_rain_given_trafficvol_gt_3000 * p_traffic_gt_3000) / p_rain

    print(f"Probability of traffic volume > 3000 given that it's raining: {p_trafficvol_gt_3000_given_rain:.4f}")

    #double-check
    traffic_gt_3000_and_rain= len(df[(df['traffic_volume'] > 3000) & (df['weather_main'] == 'Rain')])
    p_traffic_gt_3000_given_rain=traffic_gt_3000_and_rain/len(df[df['weather_main'] == 'Rain'])
    print(p_traffic_gt_3000_given_rain)