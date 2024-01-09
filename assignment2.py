#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
import re

# Connect to SQLite database
conn = sqlite3.connect('email_counts.db')
c = conn.cursor()

# Create table to store counts
c.execute('''CREATE TABLE IF NOT EXISTS Counts 
             (org TEXT, count INTEGER)''') 

# Open mbox.txt and read lines
f = open('mbox.txt','r')
lines = f.readlines()
f.close()

# Initialize dictionary to store email counts
counts = {}

# Loop through mbox lines
for line in lines:
    if line.startswith('From '):
        # Extract email address and domain
        email = re.findall(r'<\S+@(\S+)>', line)[0]
        domain = email.split('@')[1]
        
        # Increment count for domain
        if domain not in counts:
            counts[domain] = 1
        else:
            counts[domain] += 1
            
# Insert counts into database
for domain,count in counts.items():
    c.execute('INSERT INTO Counts (org, count) VALUES (?,?)', (domain,count))
    
# Commit changes and close connection
conn.commit()
conn.close()

print("Counts:")
for row in c.execute('SELECT * FROM Counts'):
    print(row[0], row[1])

