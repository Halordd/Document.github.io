import sqlite3
import csv
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Tên tệp cơ sở dữ liệu
db_name = 'water_quality.db'

# Kiểm tra nếu tệp cơ sở dữ liệu đã tồn tại thì xóa nó
if os.path.exists(db_name):
    os.remove(db_name)
    print(f"Cơ sở dữ liệu '{db_name}' đã bị xóa.")

# Kết nối với cơ sở dữ liệu SQLite (nó sẽ tạo cơ sở dữ liệu mới)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Tạo bảng nếu chưa tồn tại
cursor.execute('''
CREATE TABLE IF NOT EXISTS water_quality (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ph REAL,
    hardness REAL,
    solids REAL,
    chloramines REAL,
    sulfate REAL,
    conductivity REAL,
    organic_carbon REAL,
    trihalomethanes REAL,
    turbidity REAL,
    potability INTEGER
)
''')

# Đọc tệp CSV để tính giá trị trung bình của từng cột
def calculate_column_means(file_path):
    column_sums = [0] * 10
    column_counts = [0] * 10
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Bỏ qua dòng tiêu đề
        for row in csv_reader:
            for i in range(10):
                try:
                    value = float(row[i])  # Thử chuyển đổi giá trị thành float
                    column_sums[i] += value
                    column_counts[i] += 1
                except (ValueError, IndexError):
                    continue  # Bỏ qua các giá trị không hợp lệ hoặc thiếu
    column_means = [column_sums[i] / column_counts[i] if column_counts[i] > 0 else None for i in range(10)]
    return column_means

# Thêm dữ liệu từ tệp CSV, thay thế các giá trị null bằng trung bình của cột
def add_data_from_csv(file_path, column_means):
    if not os.path.isfile(file_path):
        print(f"Tệp '{file_path}' không tồn tại.")
        return
    
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Bỏ qua dòng tiêu đề
        for row in csv_reader:
            sanitized_row = []
            for i, value in enumerate(row):
                # Nếu giá trị null, thay thế bằng trung bình của cột; nếu không, chuyển đổi giá trị thành số
                if value is None or value.strip() == '':
                    sanitized_value = column_means[i]
                else:
                    try:
                        sanitized_value = float(value)
                    except ValueError:
                        sanitized_value = None  # Giữ None nếu giá trị không hợp lệ
                sanitized_row.append(sanitized_value)
                
            # Thêm hàng đã làm sạch vào bảng
            cursor.execute('''
            INSERT INTO water_quality (ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, potability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sanitized_row)
    conn.commit()

# Sử dụng hộp thoại chọn tệp để lấy đường dẫn tệp
def select_csv_file():
    Tk().withdraw()  # Ẩn cửa sổ chính của Tkinter
    file_path = askopenfilename(
        title="Chọn tệp CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

# Gọi hàm để chọn tệp CSV
csv_file_path = select_csv_file()

# Kiểm tra nếu người dùng đã chọn tệp thì thêm dữ liệu
if csv_file_path:
    column_means = calculate_column_means(csv_file_path)  # Tính giá trị trung bình của mỗi cột
    add_data_from_csv(csv_file_path, column_means)  # Thêm dữ liệu với giá trị trung bình thay thế
else:
    print("Bạn chưa chọn tệp nào.")

# Đóng kết nối sau khi hoàn tất
conn.close()
