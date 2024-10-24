from scipy.stats import ttest_ind, t
import sqlite3
import pandas as pd

# Kết nối đến cơ sở dữ liệu SQLite
db_path = 'water_quality.db'
conn = sqlite3.connect(db_path)

# Đọc dữ liệu từ cơ sở dữ liệu vào DataFrame
query = "SELECT * FROM water_quality"
df = pd.read_sql_query(query, conn)

# Đóng kết nối đến cơ sở dữ liệu
conn.close()

# Tách dữ liệu dựa trên giá trị potability
drinkable = df[df['potability'] == 1]
non_drinkable = df[df['potability'] == 0]

# Mức ý nghĩa
alpha = 0.05

# Thực hiện kiểm định t-test cho từng cột số
t_test_results_filtered = {}
for column in df.columns:
    if column not in ['potability', 'id'] and pd.api.types.is_numeric_dtype(df[column]):
        # Thực hiện kiểm định t-test
        t_stat, p_value = ttest_ind(drinkable[column].dropna(), non_drinkable[column].dropna(), equal_var=False)
        
        # Tính bậc tự do
        n1 = len(drinkable[column].dropna())
        n2 = len(non_drinkable[column].dropna())
        df_value = n1 + n2 - 2
        
        t_critical = t.ppf(1 - alpha/2, df_value)
        
        # Lưu kết quả
        t_test_results_filtered[column] = {
            'T-statistic': t_stat,
            'p-value': p_value,
            'Critical T-value (0.05)': t_critical,
            'Significant Difference (95%)': p_value < 0.05
        }

# Chuyển kết quả sang DataFrame để dễ đọc hơn
t_test_results_filtered_df = pd.DataFrame(t_test_results_filtered).T

# Hiển thị kết quả
print(t_test_results_filtered_df)
