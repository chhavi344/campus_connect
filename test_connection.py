# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:51:17 2026

@author: Lenovo
"""

from database import get_connection

try:

    connection = get_connection()

    print("Database Connected Successfully")

    connection.close()

except Exception as e:

    print(e)