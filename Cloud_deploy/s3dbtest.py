import boto3
import pandas
import sqlite3

s3 = boto3.resource('s3')

cnx = sqlite3.connect('s3://databasewithsqlite/test.db')