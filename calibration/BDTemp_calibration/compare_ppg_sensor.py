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
    # Resample ทุกคอลัมน์ที่ต้องการ
    df_resampled = df.set_index('Timestamp').resample(rule).agg({
        'BodyTemp(C)': ['mean', 'min', 'max'],
        'T1': ['mean', 'min', 'max'],
        'TH': ['mean', 'min', 'max']
    }).round(2)
    df_resampled.columns = [
        'BodyTemp_Mean', 'BodyTemp_Min', 'BodyTemp_Max',
        'T1_Mean', 'T1_Min', 'T1_Max',
        'TH_Mean', 'TH_Min', 'TH_Max'
    ]
    df_resampled = df_resampled.reset_index()

    plt.figure(figsize=(14, 6))
    # BodyTemp(C)
    plt.plot(df_resampled['Timestamp'], df_resampled['BodyTemp_Mean'], 'r', label='BodyTemp Mean')
    plt.plot(df_resampled['Timestamp'], df_resampled['BodyTemp_Min'], 'r--', label='BodyTemp Min', alpha=0.7)
    plt.plot(df_resampled['Timestamp'], df_resampled['BodyTemp_Max'], 'r:', label='BodyTemp Max', alpha=0.7)
    # T1
    plt.plot(df_resampled['Timestamp'], df_resampled['T1_Mean'], 'g', label='T1 Mean')
    plt.plot(df_resampled['Timestamp'], df_resampled['T1_Min'], 'g--', label='T1 Min', alpha=0.7)
    plt.plot(df_resampled['Timestamp'], df_resampled['T1_Max'], 'g:', label='T1 Max', alpha=0.7)
    # TH
    plt.plot(df_resampled['Timestamp'], df_resampled['TH_Mean'], 'b', label='TH Mean')
    plt.plot(df_resampled['Timestamp'], df_resampled['TH_Min'], 'b--', label='TH Min', alpha=0.7)
    plt.plot(df_resampled['Timestamp'], df_resampled['TH_Max'], 'b:', label='TH Max', alpha=0.7)

    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Comparison (Resample {interval} seconds)')
    plt.legend(frameon=True, loc='upper right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='major', axis='x', linestyle='-', alpha=0.3)
    plt.tight_layout()
    plt.show()