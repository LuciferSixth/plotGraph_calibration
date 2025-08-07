import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# อ่านข้อมูลจากไฟล์
df = pd.read_csv('Body_Temp_Log__600_rows_.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S')

# กำหนดช่วงเวลาที่ต้องการ resample
intervals = [5, 10, 20, 30]  # วินาที

for interval in intervals:
    rule = f'{interval}s'
    # Resample เฉพาะค่า mean
    df_resampled = df.set_index('Timestamp').resample(rule).agg({
        'BodyTemp(C)': 'mean',
        'T1': 'mean',
        'TH': 'mean'
    }).reset_index()
    df_resampled.columns = ['Timestamp', 'BodyTemp_Mean', 'T1_Mean', 'TH_Mean']

    # Plot Mean only
    plt.figure(figsize=(14, 6))
    plt.plot(df_resampled['Timestamp'], df_resampled['BodyTemp_Mean'], 'r', label='BodyTemp Mean', linewidth=2)
    plt.plot(df_resampled['Timestamp'], df_resampled['T1_Mean'], 'g', label='T1 Mean', linewidth=2)
    plt.plot(df_resampled['Timestamp'], df_resampled['TH_Mean'], 'b', label='TH Mean', linewidth=2)

    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Comparison (Mean, Resample {interval} seconds)')
    plt.legend(frameon=True, loc='upper right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='major', axis='x', linestyle='-', alpha=0.3)
    plt.tight_layout()
    plt.show()