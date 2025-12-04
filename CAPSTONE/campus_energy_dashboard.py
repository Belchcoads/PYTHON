# Campus Energy-Use Dashboard - Capstone Project
# Name: Deepanshu Gulia
# Roll No.: 2501730335
# Course: BTECH CSE (AIML)
# Subject: Programming for Problem Solving using Python

import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd
import matplotlib.pyplot as plt


# =========================
# Task 3: OOP Modeling
# =========================

@dataclass
class MeterReading:
    timestamp: pd.Timestamp
    kwh: float


class Building:
    def __init__(self, name: str):
        self.name = name
        self.meter_readings: List[MeterReading] = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self) -> float:
        return sum(r.kwh for r in self.meter_readings)

    def to_dataframe(self) -> pd.DataFrame:
        data = {
            "building": [self.name] * len(self.meter_readings),
            "timestamp": [r.timestamp for r in self.meter_readings],
            "kwh": [r.kwh for r in self.meter_readings],
        }
        return pd.DataFrame(data)

    def generate_report(self) -> str:
        if not self.meter_readings:
            return f"Building {self.name}: No data available.\n"
        total = self.calculate_total_consumption()
        avg = total / len(self.meter_readings)
        return (
            f"Building: {self.name}\n"
            f"  Total consumption (kWh): {total:.2f}\n"
            f"  Average per reading (kWh): {avg:.2f}\n"
        )


class BuildingManager:
    def __init__(self):
        self.buildings: Dict[str, Building] = {}

    def get_or_create_building(self, name: str) -> Building:
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            bld_name = row["building"]
            ts = row["timestamp"]
            kwh = row["kwh"]
            building = self.get_or_create_building(bld_name)
            building.add_reading(MeterReading(ts, kwh))

    def to_dataframe(self) -> pd.DataFrame:
        frames = [b.to_dataframe() for b in self.buildings.values()]
        if frames:
            return pd.concat(frames, ignore_index=True)
        return pd.DataFrame(columns=["building", "timestamp", "kwh"])

    def generate_summary_table(self) -> pd.DataFrame:
        df = self.to_dataframe()
        if df.empty:
            return pd.DataFrame()
        summary = df.groupby("building")["kwh"].agg(
            total="sum",
            mean="mean",
            min="min",
            max="max"
        ).reset_index()
        return summary

    def generate_text_report(self) -> str:
        lines = []
        for building in self.buildings.values():
            lines.append(building.generate_report())
        return "\n".join(lines)


# =========================
# Task 1: Data Ingestion and Validation
# =========================

def load_energy_data(data_dir: Path) -> pd.DataFrame:
    all_frames = []
    errors = []

    if not data_dir.exists():
        print(f"Data directory {data_dir} not found.")
        return pd.DataFrame()

    for csv_file in data_dir.glob("*.csv"):
        try:
            # Try to read CSV
            df = pd.read_csv(csv_file)

            # Basic validation: must contain kwh column
            if "kwh" not in df.columns:
                print(f"Skipping {csv_file.name}: no 'kwh' column.")
                errors.append(f"No kwh column in {csv_file.name}")
                continue

            # Handle timestamp column
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            elif "date" in df.columns:
                df["timestamp"] = pd.to_datetime(df["date"], errors="coerce")
            else:
                print(f"Skipping {csv_file.name}: no timestamp/date column.")
                errors.append(f"No timestamp column in {csv_file.name}")
                continue

            # Drop rows with invalid timestamps
            df = df.dropna(subset=["timestamp"])

            # Add building name if missing
            if "building" not in df.columns:
                building_name = csv_file.stem  # filename without .csv
                df["building"] = building_name

            all_frames.append(df)

        except FileNotFoundError:
            msg = f"File not found: {csv_file}"
            print(msg)
            errors.append(msg)
        except Exception as e:
            msg = f"Error reading {csv_file.name}: {e}"
            print(msg)
            errors.append(msg)

    if not all_frames:
        print("No valid CSV files found.")
        return pd.DataFrame()

    combined = pd.concat(all_frames, ignore_index=True)

    # Optional: print errors log
    if errors:
        print("\nIngestion issues:")
        for e in errors:
            print(" -", e)

    return combined


# =========================
# Task 2: Aggregation Logic
# =========================

def calculate_daily_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.set_index("timestamp")
    daily = df.resample("D")["kwh"].sum().reset_index()
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.set_index("timestamp")
    weekly = df.resample("W")["kwh"].sum().reset_index()
    return weekly


def building_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    summary = df.groupby("building")["kwh"].agg(
        total="sum",
        mean="mean",
        min="min",
        max="max"
    ).reset_index()
    return summary


# =========================
# Task 4: Visualization
# =========================

def create_dashboard_plots(df: pd.DataFrame, output_path: Path):
    if df.empty:
        print("No data available for plotting.")
        return

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # Figure with 3 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax1 = axes[0, 0]
    ax2 = axes[0, 1]
    ax3 = axes[1, 0]

    # 1) Trend line – daily consumption over time for all buildings
    daily = calculate_daily_totals(df)
    ax1.plot(daily["timestamp"], daily["kwh"], marker="o")
    ax1.set_title("Daily Campus Consumption")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")

    # 2) Bar chart – average weekly usage across buildings
    df.set_index("timestamp", inplace=True)
    weekly_building = df.groupby("building").resample("W")["kwh"].sum().reset_index()
    weekly_avg = weekly_building.groupby("building")["kwh"].mean().reset_index()
    ax2.bar(weekly_avg["building"], weekly_avg["kwh"])
    ax2.set_title("Average Weekly Usage per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average Weekly kWh")
    ax2.tick_params(axis="x", rotation=45)

    # 3) Scatter plot – peak-hour consumption vs building
    df_reset = df.reset_index()
    df_reset["hour"] = df_reset["timestamp"].dt.hour
    peak_by_building = df_reset.groupby(["building", "hour"])["kwh"].max().reset_index()
    # For scatter: x = hour, y = kwh, color/group = building
    for bld in peak_by_building["building"].unique():
        subset = peak_by_building[peak_by_building["building"] == bld]
        ax3.scatter(subset["hour"], subset["kwh"], label=bld)
    ax3.set_title("Peak-Hour Consumption by Building")
    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("kWh")
    ax3.legend(fontsize="small", loc="best")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Dashboard plot saved to: {output_path}")


# =========================
# Task 5: Persistence and Summary
# =========================

def generate_executive_summary(df: pd.DataFrame,
                               building_summary_df: pd.DataFrame,
                               output_path: Path):
    if df.empty:
        text = "No data available for summary.\n"
        output_path.write_text(text, encoding="utf-8")
        print(f"Summary written to: {output_path}")
        return

    total_campus = df["kwh"].sum()

    # Highest consuming building
    if not building_summary_df.empty:
        top_row = building_summary_df.sort_values("total", ascending=False).iloc[0]
        top_building = top_row["building"]
        top_consumption = top_row["total"]
    else:
        top_building = "N/A"
        top_consumption = 0

    # Peak load time (timestamp with highest kwh)
    max_row = df.loc[df["kwh"].idxmax()]
    peak_time = max_row["timestamp"]
    peak_value = max_row["kwh"]

    # Daily and weekly trend short description
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)

    summary_lines = [
        "Campus Energy-Use Executive Summary",
        "-----------------------------------",
        f"Total campus consumption (kWh): {total_campus:.2f}",
        f"Highest-consuming building: {top_building} ({top_consumption:.2f} kWh)",
        f"Peak load time: {peak_time} with {peak_value:.2f} kWh",
        "",
        f"Number of days in dataset: {len(daily)}",
        f"Number of weeks in dataset: {len(weekly)}",
    ]

    output_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"Summary written to: {output_path}")


# =========================
# Main Pipeline
# =========================

def main():
    base_dir = Path(".")
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Task 1: Load and validate data
    print("Loading energy data...")
    df = load_energy_data(data_dir)
    if df.empty:
        print("No data to process. Exiting.")
        return

    # Ensure correct types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
    df = df.dropna(subset=["kwh"])
    df["building"] = df["building"].astype(str)

    # Task 3: Build OOP model
    manager = BuildingManager()
    manager.load_from_dataframe(df)

    # Task 2: Aggregations
    building_summary_df = manager.generate_summary_table()

    # Save cleaned data and summary
    cleaned_path = output_dir / "cleaned_energy_data.csv"
    summary_path = output_dir / "building_summary.csv"
    df.to_csv(cleaned_path, index=False)
    building_summary_df.to_csv(summary_path, index=False)
    print(f"Cleaned data saved to: {cleaned_path}")
    print(f"Building summary saved to: {summary_path}")

    # Task 4: Visual dashboard
    dashboard_path = output_dir / "dashboard.png"
    create_dashboard_plots(df.copy(), dashboard_path)

    # Task 5: Executive summary
    summary_txt_path = output_dir / "summary.txt"
    generate_executive_summary(df, building_summary_df, summary_txt_path)

    # Optional: print per-building text report
    print("\nPer-building report:")
    print(manager.generate_text_report())


if __name__ == "__main__":
    main()
