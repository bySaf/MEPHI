import psycopg2

connection = psycopg2.connect(user="osg",
                              password="111",
                              host="localhost",
                              port="5432",
                              database= "test")

connection.autocommit = True

cursor = connection.cursor()


for i in range(1):
    a = input().split()
    b = str(a[0])
    c = str(a[1])
    d = int(a[2])
    cursor.execute(f"INSERT INTO courses(c_no, title, hours) VALUES ('{b}', '{c}', {d});")
cursor.close()
connection.close()
print("z")
