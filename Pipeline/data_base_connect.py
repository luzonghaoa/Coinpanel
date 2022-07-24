import psycopg2

def connect():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="coin_panel_test")
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect", error)

if __name__ == '__main__':
    connection = connect()
    cursor = connection.cursor()
    query = """ CREATE TABLE IF NOT EXISTS price_kline (
                                            symbol varchar(10)
                                            , start_time timestamp
                                            , close_time timestamp
                                            , interval varchar(5)
                                            , low_price real
                                            , high_price real
                                            , close_price real
                                            )
                                            """
    cursor.execute(query)
    connection.commit()
    #print(count, "Record inserted successfully into mobile table")