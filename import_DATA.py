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

# Hàm để chuyển các giá trị trống hoặc không hợp lệ thành None
def sanitize_value(value):
    if value is None or value.strip() == '':
        return None
    try:
        # Thử chuyển đổi giá trị thành số thực (float) hoặc số nguyên (int)
        return float(value)
    except ValueError:
        return value

# Thêm dữ liệu từ tệp CSV
def add_data_from_csv(file_path):
    if not os.path.isfile(file_path):
        print(f"Tệp '{file_path}' không tồn tại.")
        return
    
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Bỏ qua dòng tiêu đề
        for row in csv_reader:
            # Áp dụng hàm sanitize_value cho từng giá trị trong dòng
            row = [sanitize_value(value) for value in row]
            cursor.execute('''
            INSERT INTO water_quality (ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, potability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
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
    add_data_from_csv(csv_file_path)
else:
    print("Bạn chưa chọn tệp nào.")

# Đóng kết nối sau khi hoàn tất
conn.close()
