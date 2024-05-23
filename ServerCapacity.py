import json

#Read in JSON file
capcistyJSONFile = open("oneview_ServerHardware_500plus.txt", "r")
capacityJSONText = capcistyJSONFile.read()
capacityJSON = json.loads(capacityJSONText)
capcistyJSONFile.close()

membersList = capacityJSON["members"]

with open('serverCapacityplus.csv', 'w') as outputFile:
    print("SerialNumber,Capacity", file=outputFile)
    for member in membersList:
        serialNumber = member["serialNumber"]
        #print(serialNumber)

        dataList = member["subResources"]["LocalStorage"]["data"]
        if dataList is not None:
            for data in dataList:
                #model = data["Model"]
                #print(serialNumber + " - " + model)
                if "LogicalDrives" in data:
                    logicalDriveList = data["LogicalDrives"]
                    for logicalDrive in logicalDriveList:
                        if "CapacityMiB" in logicalDrive:
                            print(serialNumber + "," + str(logicalDrive["CapacityMiB"] / 1000), file=outputFile)
                        elif "CapacityGB" in logicalDrive:
                            print(serialNumber + "," + str(logicalDrive["CapacityGB"]), file=outputFile)
                        else:
                            print(serialNumber + "," + "0", file=outputFile)