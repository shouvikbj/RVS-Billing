import json
import os
import nanoid
import uuid
import copy


def signupUser(APP_ROOT, email, name, password):
    json_file = open(f"{APP_ROOT}/db/login.json", "r")
    users = json.load(json_file)
    backup = copy.deepcopy(users)
    json_file.close()
    resp = {}
    for user in users:
        if user["email"] == email:
            resp = {"status": "not-ok", "message": "Email already in use!"}
            return resp
    try:
        data = {
            "id": str(nanoid.generate()),
            "email": email,
            "name": name,
            "password": password,
        }
        users.append(data)
        json_file = open(f"{APP_ROOT}/db/login.json", "w")
        json_file.seek(0)
        json.dump(users, json_file, indent=2)
        json_file.close()
        resp = {"status": "ok", "message": "Signup successful!"}
        return resp
    except Exception:
        json_file = open(f"{APP_ROOT}/db/login.json", "w")
        json_file.seek(0)
        json.dump(backup, json_file, indent=2)
        json_file.close()
        resp = {"status": "not-ok", "message": "Signup failed!"}
        return resp


def checkAuth(APP_ROOT, email, password):
    json_file = open(f"{APP_ROOT}/db/login.json", "r")
    users = json.load(json_file)
    json_file.close()
    resp = {}
    for user in users:
        if user["email"] == email and user["password"] == password:
            resp = {"status": "ok", "message": "Login successful!", "user": user}
            return resp
    resp = {"status": "not-ok", "message": "Invalid credentials!"}
    return resp