from typing import Tuple, Any

import psycopg2


class DataBase:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(user="postgres",
                                           password="sirius",
                                           host="localhost",
                                           port="5432",
                                           database="project")

        self.connection.autocommit = True

        self.cursor = self.connection.cursor()

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS connection_losses(
            id INT PRIMARY KEY,
            RPI_id INT,
            moment DATE,
            clock TIME
            )      
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS main_table(
            id INT PRIMARY KEY,
            RPI_id INT,
            moment DATE,
            starting TIME,
            ending TIME,
            result INT,
            checking INT
            )      
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users_base(
            id INT PRIMARY KEY,
            fullname TEXT,
            username TEXT,
            password TEXT,
            role TEXT
            )
            '''
        )

        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users_logs(
            id INT PRIMARY KEY,
            username TEXT,
            moment DATE,
            starting TIME,
            ending TIME
            )
            '''
        )

    def add_incident(self, rpi_id, moment, starting) -> None:
        self.cursor.execute(
            """
            INSERT INTO main_table(rpi_id, moment, starting)
            VALUES(%s, %s, %s);
            """, (rpi_id, moment, starting))

    def update_time_of_incident(self, ending, starting) -> None:
        self.cursor.execute(
            """
            UPDATE main_table
            SET ending = %s
            WHERE starting = %s
            """, (ending, starting))

    def update_data_of_incident(self, data, starting) -> None:
        self.cursor.execute(
            """
            UPDATE main_table
            SET data = %s
            WHERE starting = %s
            """, (data, starting))

    def get_name_of_incident(self, starting) -> str:
        self.cursor.execute(
            """
            SELECT id, moment 
            FROM main_table
            WHERE starting = %s
            """, (starting, )
        )
        data = self.cursor.fetchall()
        return f"{data[0][0]}-{data[0][1]}"



