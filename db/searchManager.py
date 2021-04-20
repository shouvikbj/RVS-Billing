import json
import os


def searchDistributor(APP_ROOT, creatorEmail, searchText):
    with open(f"{APP_ROOT}/db/distributor.json", "r") as json_file:
        distributorList = json.load(json_file)
    resp = []
    if searchText == "":
        return []
    for distributor in distributorList:
        if (
            creatorEmail == distributor["creatorEmail"]
            and searchText.lower() in distributor["name"].lower()
        ):
            resp.append(distributor)
    return resp


def searchReport(APP_ROOT, creatorEmail, year):
    monthsList = [
        {"name": "January", "billAmount": 0, "actualPayment": 0},
        {"name": "February", "billAmount": 0, "actualPayment": 0},
        {"name": "March", "billAmount": 0, "actualPayment": 0},
        {"name": "April", "billAmount": 0, "actualPayment": 0},
        {"name": "May", "billAmount": 0, "actualPayment": 0},
        {"name": "June", "billAmount": 0, "actualPayment": 0},
        {"name": "July", "billAmount": 0, "actualPayment": 0},
        {"name": "August", "billAmount": 0, "actualPayment": 0},
        {"name": "September", "billAmount": 0, "actualPayment": 0},
        {"name": "October", "billAmount": 0, "actualPayment": 0},
        {"name": "November", "billAmount": 0, "actualPayment": 0},
        {"name": "December", "billAmount": 0, "actualPayment": 0},
    ]
    distList = []
    with open(f"{APP_ROOT}/db/distributor.json", "r") as json_file:
        distributorList = json.load(json_file)
    for distributor in distributorList:
        if distributor["creatorEmail"] == creatorEmail:
            distList.append(distributor)
    for dist in distList:
        distributorName = dist["name"]
        with open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "r",
        ) as json_file:
            bills = json.load(json_file)
            for bill in bills:
                if bill["date"][6:10] == year:
                    if bill["date"][3:5] == "01":
                        monthsList[0]["billAmount"] += int(bill["billAmount"])
                        monthsList[0]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "02":
                        monthsList[1]["billAmount"] += int(bill["billAmount"])
                        monthsList[1]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "03":
                        monthsList[2]["billAmount"] += int(bill["billAmount"])
                        monthsList[2]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "04":
                        monthsList[3]["billAmount"] += int(bill["billAmount"])
                        monthsList[3]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "05":
                        monthsList[4]["billAmount"] += int(bill["billAmount"])
                        monthsList[4]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "06":
                        monthsList[5]["billAmount"] += int(bill["billAmount"])
                        monthsList[5]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "07":
                        monthsList[6]["billAmount"] += int(bill["billAmount"])
                        monthsList[6]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "08":
                        monthsList[7]["billAmount"] += int(bill["billAmount"])
                        monthsList[7]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "09":
                        monthsList[8]["billAmount"] += int(bill["billAmount"])
                        monthsList[8]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "10":
                        monthsList[9]["billAmount"] += int(bill["billAmount"])
                        monthsList[9]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "11":
                        monthsList[10]["billAmount"] += int(bill["billAmount"])
                        monthsList[10]["actualPayment"] += int(bill["actualPayment"])
                    elif bill["date"][3:5] == "12":
                        monthsList[11]["billAmount"] += int(bill["billAmount"])
                        monthsList[11]["actualPayment"] += int(bill["actualPayment"])
    return monthsList
