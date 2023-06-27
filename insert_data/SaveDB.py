import sqlite3
import pandas as pd
import numpy as np

data = pd.read_csv("/Users/vuong/data-integration/warehouse/phones.csv", index_col=False, delimiter = ';')
ls = []
data = data.replace(np.nan,"")
# for item in data["square"]:
#     item = re.findall(r"(?:\d*\.\d+|\d+)", item)
#     if len(item):
#         item = float(item[0])
#         ls.append(item)
#     else:
#         item = float(0)
#         ls.append(item);
data = data.replace(np.nan,"")
conn = sqlite3.connect('test.db')
# data["square"] = ls
try:
    conn = sqlite3.connect('test.db')
    if conn.is_connected():
        cursor = conn.cursor(buffered=True)
        cursor.execute("SHOW DATABASES")
        cursor.execute("CREATE DATABASE IF NOT EXISTS dataphone;")
        cursor.execute("use dataphone;")

        #loop through the data frame
        for i,row in data.iterrows():
            sql = "INSERT INTO post (id,name,display_size,display_tech,camera,camera_selfie,ram,rom,battery,sim,operating_system,resolution,display_feature,cpu_type,weight,monitor_frequency,cpu,bluetooth,image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Insert record in Phone data")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)