import mysql.connector

conn = mysql.connector.connect(host="spbgcapital.f3322.net", user='spbgcapital', password='@Tnt7891011',
                               database='spbgcapital')
cursor = conn.cursor()
cursor.execute('create table user (id varchar(20) primary key,name varchar(20))')
