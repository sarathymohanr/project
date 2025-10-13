# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 15:17:39 2025

@author: student
"""

import jwt
import datetime
import time

SECRET_KEY = "mysecretkey"

# Create access token (expires in 5 seconds)
def create_access_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Create refresh token (expires in 30 seconds)
def create_refresh_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Refresh access token using refresh token
def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        username = payload["username"]
        print(f"[INFO] Refresh token valid for user: {username}")
        return create_access_token(username)
    except jwt.ExpiredSignatureError:
        print("[ERROR] Refresh token expired. Please log in again.")
    except jwt.InvalidTokenError:
        print("[ERROR] Invalid refresh token.")

# === Demo ===

if __name__ == "__main__":
    username = "testuser"

    print("=== Login ===")
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

    print("\n[WAIT] Waiting 6 seconds for access token to expire...")
    time.sleep(6)

    print("\n=== Validate Access Token ===")
    try:
        decoded = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        print("[OK] Access token still valid:", decoded)
    except jwt.ExpiredSignatureError:
        print("[INFO] Access token expired.")
        print("[INFO] Attempting to refresh access token...")
        new_access_token = refresh_access_token(refresh_token)
        if new_access_token:
            print("[SUCCESS] New Access Token:", new_access_token)
        else:
            print("[FAILURE] Could not refresh access token.")

