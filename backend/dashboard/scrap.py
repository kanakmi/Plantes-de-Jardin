import json
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('plants.db')


def insert_data(conn, data):
    cursor = conn.cursor()
    rows = (data[0], data[1], data[3], data[2], data[4])
    cursor.execute('INSERT INTO plants VALUES (?, ?, ?, ?, ?)', rows)

    conn.commit()


url = 'http://www.thegardenhelper.com/commindex.html'
url1 = "https://www.bing.com/images/vsasync?q="

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
results = soup.find("td", class_="c2")
job_elements = results.find_all("tr")

for job_element in job_elements:
    cname = job_element.findAll('td')
    if(len(cname) > 1):
        data = []
        data.append(cname[0].text)
        data.append(cname[1].text)
        data.append(cname[2].text)
        data.append(cname[3].text)
        try:
            a = requests.get(url1+cname[0].text)
            binary = a.content
            output = json.loads(binary)
            img = output['results'][0]['imageUrl']
            data.append(img)
        except:
            data.append(" ")
        insert_data(conn, data)
conn.close()
