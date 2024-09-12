import json
import mysql.connector
from mysql.connector import Error


def connect_to_database():
    try:
        con = mysql.connector.connect(
            host="localhost", user="root", passwd="", port=3306, database="tenders"
        )
        print("Connected to database")
        return con
    except Exception as e:
        print("Error connecting to database:", e)
        return None


def insert_data(con, data):
    if con:
        cur = con.cursor()
        try:
            for item in data:
                sql_query = """INSERT INTO tenders (category, description, eSubmission, `Tender Number`, Department, `Tender Type`, Province, `Date Published`, `Closing Date`, `Place where goods, works or services are required`, `Special Conditions`, `Contact Person`, Email, `Telephone number`, `FAX Number`, `Is there a briefing session?`, `Is it compulsory?`, `Briefing Date and Time`, `Briefing Venue`) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    item.get("category"),
                    item.get("description"),
                    item.get("eSubmission"),
                    item.get("Tender Number"),
                    item.get("Department"),
                    item.get("Tender Type"),
                    item.get("Province"),
                    item.get("Date Published"),
                    item.get("Closing Date"),
                    item.get("Place where goods, works or services are required"),
                    item.get("Special Conditions"),
                    item.get("Contact Person"),
                    item.get("Email"),
                    item.get("Telephone number"),
                    item.get("FAX Number"),
                    item.get("Is there a briefing session?"),
                    item.get("Is it compulsory?"),
                    item.get("Briefing Date and Time"),
                    item.get("Briefing Venue"),
                )
                # print("\n")
                # print("Number of values:", len(values))
                # print("Executing SQL query:", sql_query)
                # print("Values:", values)
                cur.execute(sql_query, values)
            con.commit()
            print("Data inserted successfully.")
        except Exception as e:
            con.rollback()
            print("Error inserting data:", e)
        finally:
            cur.close()
            con.close()
    else:
        print("Failed to connect to database.")


with open("extracted_tenders.json", "r") as f:
    data = json.load(f)

con = connect_to_database()

insert_data(con, data)
