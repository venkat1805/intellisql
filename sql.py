# Import module 
import sqlite3 
import random

# Connecting to sqlite 
conn = sqlite3.connect('test.db') 

# Creating a cursor object using the cursor() method 
cursor = conn.cursor() 

# Creating table (drop first if exists for fresh start)
cursor.execute("DROP TABLE IF EXISTS STUDENT")

table = """
CREATE TABLE STUDENT (
    NAME VARCHAR(255),
    CLASS VARCHAR(255), 
    SECTION VARCHAR(255)
);
"""
cursor.execute(table) 

# Sample data lists
names = [
    "Karthikeya", "Bunny", "Local", "Sarswathi", "Anjali", "Vikram", "Neha", "Raghav", "Sneha", "Tejas",
    "Aarushi", "Manish", "Preeti", "Aditya", "Pooja", "Kiran", "Divya", "Nikhil", "Ishita", "Aman"
]
classes = ["Data Science", "DevOps", "AI", "Cyber Security", "Cloud", "Web Development"]
sections = ["A", "B", "C", "D"]

# Insert multiple records
for _ in range(30):
    name = random.choice(names)
    cls = random.choice(classes)
    section = random.choice(sections)
    cursor.execute("INSERT INTO STUDENT VALUES (?, ?, ?)", (name, cls, section))

# Display data inserted 
print("Data Inserted in the table:")
data = cursor.execute("SELECT * FROM STUDENT") 
for row in data: 
    print(row) 

# Commit your changes in the database     
conn.commit() 

# Closing the connection 
conn.close()
