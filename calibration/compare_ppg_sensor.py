import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read PPG Rate from 5min_addtime_with_rate.csv
ppg_df = pd.read_csv('5min_addtime_with_rate.csv')
ppg_df['Timestamp'] = pd.to_datetime(ppg_df['Timestamp'])

# Sensor values (your list)
sensor_values = [95,95,95,95,95,97,92,92,92,93,93,93,92,92,91,91,91,91,96,96,94,94,
                96,96,96,96,84,94,90,90,91,91,88,88,88,88,88,88,88,88,87,87,90,90,
                92,92,93,93,93,93,94,94,92,92,92,91,91,90,90,91,91,90,90,91,91,91,
                92,91,92,95,95,98,98,100,100,101,101,102,102,100,100,98,87,100,100,
                98,98,98,98,100,100,98,98,95,95,95,95,94,94,94,94,93,93,93,93,94,94,
                96,96,94,94,95,95,95,95,100,100,102,102,103,103,108,108,110,110,105,
                105,107,107,108,108,108,105,105,107,107,107,107,105,105,105,105,105,
                105,101,101,101,101,100,100,101]

start_time = pd.to_datetime('2025-07-26 11:42:47')
time_seconds = list(range(0, len(sensor_values) * 2, 2))
timestamps = [start_time + pd.Timedelta(seconds=s) for s in time_seconds]
sensor_df_valid = pd.DataFrame({
    'Timestamp': timestamps,
    'My sensor': sensor_values
})

# กำหนดช่วงเวลาที่ต้องการ resample
intervals = [2, 4, 6, 8, 10, 20, 30]  # วินาที

for interval in intervals:
    rule = f'{interval}S'
    # Resample PPG
    ppg_resampled = ppg_df.set_index('Timestamp').resample(rule).agg({
        'PPG_Rate': ['mean', 'min', 'max']
    }).reset_index()
    ppg_resampled.columns = ['Timestamp', 'PPG_Mean', 'PPG_Min', 'PPG_Max']

    # Resample Sensor
    sensor_resampled = sensor_df_valid.set_index('Timestamp').resample(rule).agg({
        'My sensor': ['mean', 'min', 'max']
    }).reset_index()
    sensor_resampled.columns = ['Timestamp', 'Sensor_Mean', 'Sensor_Min', 'Sensor_Max']

    # Plot
    plt.figure(figsize=(14, 6))
    plt.plot(ppg_resampled['Timestamp'], ppg_resampled['PPG_Mean'], 'orange', label='PPG Mean', linewidth=1.5)
    plt.plot(ppg_resampled['Timestamp'], ppg_resampled['PPG_Min'], 'orange', linestyle='--', label='PPG Min', alpha=0.7)
    plt.plot(ppg_resampled['Timestamp'], ppg_resampled['PPG_Max'], 'orange', linestyle=':', label='PPG Max', alpha=0.7)

    plt.plot(sensor_resampled['Timestamp'], sensor_resampled['Sensor_Mean'], 'b', label='Sensor Mean', linewidth=1.5)
    plt.plot(sensor_resampled['Timestamp'], sensor_resampled['Sensor_Min'], 'b', linestyle='--', label='Sensor Min', alpha=0.7)
    plt.plot(sensor_resampled['Timestamp'], sensor_resampled['Sensor_Max'], 'b', linestyle=':', label='Sensor Max', alpha=0.7)

    plt.xlabel('Time')
    plt.ylabel('Heart Rate (BPM)')
    plt.title(f'Comparison (Resample {interval} seconds)')
    plt.legend(frameon=True, loc='upper right')
    plt.ylim(75, 115)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='major', axis='x', linestyle='-', alpha=0.3)
    plt.tight_layout()
    plt.show()