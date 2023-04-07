import grpc
import example_pb2
import example_pb2_grpc
from config import database_auth
from concurrent import futures
import datetime

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


now = datetime.datetime.now()
print(now)
current_date = current_date_format(str(now))
print(current_date)

class DataServer(example_pb2_grpc.Data):
    
    def GetWeatherData(self, request, context):
        print("GetWeatherData")
        #extract the more refrehing time of the db
        cur.execute("SELECT * FROM weather where date = '"+ str(current_date) +"' order by id desc limit 1")
        weather = cur.fetchall()
        temperature = {
            "id": int(weather[0][0]),
            "temp": str(weather[0][1]),
            "time": str(weather[0][2]),
            "date": str(weather[0][3])
        }
        temperature_response = example_pb2.WeatherResponse(**temperature)
        return temperature_response
    
    def GetCoinsData(self, request, context):
        print("GetCoinsData")
        cur.execute("SELECT * FROM cash where date = '"+ str(current_date) +"' order by id desc limit 1")
        coins = cur.fetchall()
        coins = {
            "id": int(coins[0][0]),
            "dolar": str(coins[0][1]),
            "euro": str(coins[0][2]),
            "uf": str(coins[0][3]),
            "time": str(coins[0][4]),
            "date": str(coins[0][5])
        }
        coins_response = example_pb2.CoinsResponse(**coins)
        return coins_response
        
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_DataServicer_to_server(DataServer(), server)
    #Exponer a cualquier IP en el puerto 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("GRPC persistor server working")
    server.wait_for_termination()


if __name__ == '__main__':
    conn = database_auth.get_db()
    cur = conn.cursor()
    main()