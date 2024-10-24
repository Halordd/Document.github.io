import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
db_name = 'water_quality.db'
conn = sqlite3.connect(db_name)

# Query to fetch data
query = "SELECT * FROM water_quality"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# List of columns to analyze (excluding 'potability' since it's used for grouping)
columns = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate', 
           'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity']

# Set up the plot grid
plt.figure(figsize=(15, 12))
plt.subplots_adjust(hspace=0.5, wspace=0.4)

# Plot each parameter's distribution as KDE plots split by potability
for i, col in enumerate(columns, 1):
    plt.subplot(3, 3, i)
    sns.kdeplot(data=df[df['potability'] == 0], x=col, label='Non Potable', shade=True, color='blue')
    sns.kdeplot(data=df[df['potability'] == 1], x=col, label='Potable', shade=True, color='red')
    plt.title(f'Distribution of {col}')
    plt.legend()

# Show the plot
plt.suptitle('Distribution of Water Quality Parameters by Potability', fontsize=16)
plt.show()
