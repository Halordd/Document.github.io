import pandas as pd
import sqlite3

# Kết nối tới cơ sở dữ liệu SQLite
db_path = 'water_quality.db'  # Đường dẫn tới tệp cơ sở dữ liệu của bạn
conn = sqlite3.connect(db_path)

# Đọc dữ liệu từ bảng 'water_quality'
data_query = "SELECT * FROM water_quality;"
water_quality_data = pd.read_sql_query(data_query, conn)

# Đóng kết nối cơ sở dữ liệu
conn.close()

# Tính toán thống kê mô tả và phương sai riêng biệt cho nước uống được và không uống được
potable_data = water_quality_data[water_quality_data['potability'] == 1]
non_potable_data = water_quality_data[water_quality_data['potability'] == 0]

# Tính thống kê mô tả cơ bản
potable_stats = potable_data.describe()
non_potable_stats = non_potable_data.describe()

# Tính phương sai
potable_variance = potable_data.var()
non_potable_variance = non_potable_data.var()

# Thêm phương sai vào bảng thống kê
potable_stats.loc['variance'] = potable_variance
non_potable_stats.loc['variance'] = non_potable_variance

# Cập nhật để chỉ hiển thị giá trị đếm cho cột 'id'
potable_stats.loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'variance'], 'id'] = float('nan')
non_potable_stats.loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'variance'], 'id'] = float('nan')

# Bỏ cột 'potability' khỏi bảng thống kê
potable_stats_no_potability = potable_stats.drop(columns=['potability'], errors='ignore')
non_potable_stats_no_potability = non_potable_stats.drop(columns=['potability'], errors='ignore')

# Hiển thị kết quả
print("Potability = 1:")
print(potable_stats_no_potability)
print("\nPotability = 0:")
print(non_potable_stats_no_potability)