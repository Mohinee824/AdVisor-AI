import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse
from statsmodels.tsa.holtwinters import ExponentialSmoothing

parser = argparse.ArgumentParser()
parser.add_argument('--kpi_csv', required=True)
parser.add_argument('--out_csv', required=True)
parser.add_argument('--figures_dir', required=True)
args = parser.parse_args()

df = pd.read_csv(args.kpi_csv)
time_col = df.columns[0]
df = df.set_index(time_col)
df["is_forecast"] = 0

os.makedirs(args.figures_dir, exist_ok=True)

forecast_horizon = 10
forecast_dfs = []
plots_data = []

for col in df.drop(columns=["is_forecast"]).columns:
    series = pd.to_numeric(df[col], errors='coerce').dropna()
    if len(series) < 2:
        print(f" Skipping {col}: not enough numeric data for forecasting.")
        continue

    model = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
    forecast = model.forecast(forecast_horizon)
    residuals = series - model.fittedvalues
    stderr = residuals.std()
    lower = forecast - 1.96 * stderr
    upper = forecast + 1.96 * stderr

    forecast_df = pd.DataFrame({
        col: forecast,
        f"{col}_lower": lower,
        f"{col}_upper": upper
    })
    forecast_dfs.append(forecast_df)

    plt.figure(figsize=(8, 4))
    plt.plot(series.index, series.values, label="History")
    plt.plot(forecast.index, forecast.values, label="Forecast", linestyle="--")
    plt.fill_between(forecast.index, lower, upper, color="gray", alpha=0.3, label="95% CI")
    plt.title(f"Forecast for {col}")
    plt.xlabel(time_col)
    plt.ylabel(col)
    plt.legend()
    plt.tight_layout()

    fig_path = os.path.join(args.figures_dir, f"{col}_forecast.png")
    plt.savefig(fig_path)
    plt.close()
    print(f" Saved plot: {fig_path}")

    plots_data.append((col, series, forecast, lower, upper))

if forecast_dfs:
    forecast_all = pd.concat(forecast_dfs, axis=1)
    forecast_all["is_forecast"] = 1
    all_results = pd.concat([df, forecast_all])
    all_results.index.name = time_col
    all_results.to_csv(args.out_csv, index=True)
    print(f"\nCombined history + forecast + confidence intervals saved to: {args.out_csv}")

    n = len(plots_data)
    fig, axes = plt.subplots(n, 1, figsize=(10, 4*n), sharex=True)
    if n == 1:
        axes = [axes]

    for ax, (col, series, forecast, lower, upper) in zip(axes, plots_data):
        ax.plot(series.index, series.values, label="History")
        ax.plot(forecast.index, forecast.values, label="Forecast", linestyle="--")
        ax.fill_between(forecast.index, lower, upper, color="gray", alpha=0.3, label="95% CI")
        ax.set_title(f"Forecast for {col}")
        ax.set_ylabel(col)
        ax.legend()

    axes[-1].set_xlabel(time_col)
    plt.tight_layout()

    combined_path = os.path.join(args.figures_dir, "all_kpis_forecast.png")
    plt.savefig(combined_path)
    plt.close()
    print(f" Combined multi-panel plot saved to: {combined_path}")
else:
    print(" No valid KPI columns found for forecasting.")
