import pandas as pd

# อ่านข้อมูลจากไฟล์
df = pd.read_csv('Body_Temp_Log__600_rows_.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# กำหนดเวลาเริ่มต้นและสิ้นสุด (ปรับตามต้องการ)
start_time = df['Timestamp'].min()
end_time = df['Timestamp'].max()

# กรองข้อมูลในช่วงเวลาที่ต้องการ
mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)
df_filtered = df[mask]

# จัดกลุ่มข้อมูลทุก 5 วินาที และคำนวณค่าสถิติ
df_resampled = df_filtered.set_index('Timestamp').resample('5S').agg({
    'BodyTemp(C)': ['mean', 'min', 'max'],
    'T1': ['mean', 'min', 'max'],
    'TH': ['mean', 'min', 'max']
}).round(2)

# ปรับรูปแบบคอลัมน์
df_resampled.columns = [
    'BodyTemp_Mean_Rate', 'BodyTemp_Min_Rate', 'BodyTemp_Max_Rate',
    'T1_Mean_Rate', 'T1_Min_Rate', 'T1_Max_Rate',
    'TH_Mean_Rate', 'TH_Min_Rate', 'TH_Max_Rate'
]
df_resampled = df_resampled.reset_index()

# บันทึกผลลัพธ์
df_resampled.to_csv('every5second_temp_stats.csv', index=False)

# แสดงผลลัพธ์
print("\nAnalysis of BodyTemp, T1, TH every 5 seconds (Mean_Rate, Min_Rate, Max_Rate):")
print(df_resampled.head())

print(f"\nTotal 5-second intervals analyzed: {len(df_resampled)}")