
# Weather Data Visualizer (Auto CSV Fix Version)
# Name: Deepanshu Gulia
# Roll No: 2501730335

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# AUTO CREATE CSV IF MISSING OR EMPTY
# -----------------------------
file_name = "weather.csv"

if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
    print("weather.csv not found or empty. Creating new sample dataset...")
    with open(file_name, "w") as f:
        f.write("Date,Temperature,Rainfall\n")
        f.write("2024-01-01,18,2.5\n")
        f.write("2024-01-02,19,0.0\n")
        f.write("2024-01-03,17,1.2\n")
        f.write("2024-01-04,20,0.0\n")
        f.write("2024-01-05,21,3.1\n")
        f.write("2024-01-06,22,0.5\n")
        f.write("2024-01-07,23,1.0\n")

# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv(file_name)

print("\nDataset Preview:")
print(df.head())

# -----------------------------
# DATA CLEANING
# -----------------------------
df.dropna(inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# STATISTICAL ANALYSIS
# -----------------------------
mean_temp = np.mean(df["Temperature"])
max_temp = np.max(df["Temperature"])
min_temp = np.min(df["Temperature"])
std_temp = np.std(df["Temperature"])

print("\nTemperature Statistics:")
print("Mean:", mean_temp)
print("Max:", max_temp)
print("Min:", min_temp)
print("Standard Deviation:", std_temp)

# -----------------------------
# VISUALIZATION
# -----------------------------
plt.figure()
plt.plot(df["Date"], df["Temperature"])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.savefig("daily_temperature.png")
plt.close()

monthly_rainfall = df.groupby(df["Date"].dt.month)["Rainfall"].sum()
plt.figure()
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.title("Monthly Rainfall Totals")
plt.xlabel("Month")
plt.ylabel("Total Rainfall")
plt.savefig("monthly_rainfall.png")
plt.close()

# -----------------------------
# EXPORT CLEANED DATA
# -----------------------------
df.to_csv("cleaned_weather_data.csv", index=False)

print("\n✅ Analysis complete.")
print("✅ Files created:")
print("daily_temperature.png")
print("monthly_rainfall.png")
print("cleaned_weather_data.csv")
