#!/usr/bin/env python

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from faker import Faker
import argparse


def get_fake_user():
    faker = Faker()
    profile = faker.simple_profile()
    profile['uuid'] = faker.uuid4()
    profile['password'] = faker.md5()
    return profile


def run(user, password, host):
    # Create DB
    conn = psycopg2.connect(
        database="template1", user=user, password=password, host=host, port='5432'

    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS SQEAKDB;")
    cursor.execute("CREATE DATABASE SQEAKDB;")
    conn.close()

    # Establishing the connection
    conn = psycopg2.connect(
        database="sqeakdb", user=user, password=password, host=host, port='5432'
    )

    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS USERS")

    # Creating table as per requirement
    sql = '''CREATE TABLE USERS(
        ID VARCHAR(255),
        NAME VARCHAR(255),
        EMAIL VARCHAR(255),
        PASSWORD VARCHAR(255)
    )'''
    cursor.execute(sql)

    for i in range(100):
        fake = get_fake_user()
        # Preparing SQL queries to INSERT a record into the database.
        cursor.execute("INSERT INTO USERS(ID, NAME, EMAIL, PASSWORD) VALUES ('{}', '{}', '{}', '{}')".
                       format(fake.get('uuid'), fake.get('name'), fake.get('mail'), fake.get('password')))

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool to fill up database with fake data')

    parser.add_argument('--user',
                        required=True)
    parser.add_argument('--password',
                        required=True)
    parser.add_argument('--host',
                        required=True)

    args = parser.parse_args()

    run(args.user, args.password, args.host)
