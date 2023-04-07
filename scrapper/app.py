from flask import Flask, request, jsonify
from flask_cors import CORS
from config import database_auth
import requests, re, time, datetime
from bs4 import BeautifulSoup


def current_date_format(date):
    
    months = { 1: "Jan", 2: "Feb", 3:  "Mar", 4: "Apr", 
               5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
               9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec" }
    year = date.split("-")[0]
    #print(year)
    month = date.split("-")[1]
    #print(month)
    day = date.split("-")[2]
    #print(day)
    day = day.split(" ")[0]
    time = date.split(" ")[1]
    #print(time)
    #parse month str to int
    message = day + "-" + months[int(month)] + "-" + year
    return message

number_pattern = "^\\d+$"
re.match(number_pattern, "42")
re.match(number_pattern, "notanumber")

number_extract_pattern = "\\d+"

app = Flask(__name__)
CORS(app)
    

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'


def weather():
    
    city = "Santiago%20Chile"
    
    link = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(link).content
    
    #getting rough data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    temp = re.findall(number_extract_pattern, temp)[0]
    epoch_time = float(int(time.time()))
    fecha = (str(datetime.datetime.now()))
    fecha = current_date_format(fecha)
    print(type(fecha))
    #INsert into DB
    cur.execute("INSERT INTO weather (temp, time, date) VALUES (%s, %s, %s)", (temp, epoch_time, fecha))
    conn.commit()
    #Confirmation
    epoch_time = 0
    return print("Temp: " + temp + " Time: " + str(epoch_time))

def cash():
    
    #ULS for cash
    link = "https://www.google.com/search?q="+"dolar clp"
    link2 = "https://www.google.com/search?q="+"euro clp"
    link3 = "https://www.google.com/search?q="+"uf clp"
    
    #Getting data
    html = requests.get(link).content
    soup = BeautifulSoup(html, 'html.parser')
    dolar_arr = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    aux = dolar_arr.split(' ')
    dolar = aux[0]
    html = requests.get(link2).content
    soup = BeautifulSoup(html, 'html.parser')
    euro_arr = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    aux = euro_arr.split(' ')
    euro = aux[0]
    html = requests.get(link3).content
    soup = BeautifulSoup(html, 'html.parser')
    uf_arr = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    aux = uf_arr.split(' ')
    uf = aux[0]
    epoch_time = float(int(time.time()))
    fecha = str(datetime.datetime.now())
    fecha = current_date_format(fecha)
    #Insert into DB
    cur.execute("INSERT INTO cash (dolar, euro, uf, time, date) VALUES (%s, %s, %s, %s, %s)", (dolar, euro, uf, epoch_time, fecha))
    conn.commit()
    #Confirmation
    print("Dolar: " + dolar + " Euro: " + euro + " UF: " + uf + " Time: " + str(epoch_time))
    epoch_time = 0
    return print("Dolar: " + dolar + " Euro: " + euro + " UF: " + uf + " Time: " + str(epoch_time))

@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    cur.execute("SELECT * FROM cash")
    cash = cur.fetchall()
    cur.execute("SELECT * FROM weather")
    weather = cur.fetchall()
    return jsonify({'cash': cash, 'weather': weather})

if __name__ == '__main__':
    conn = database_auth.get_db()
    cur = conn.cursor()
    weather()
    cash()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)