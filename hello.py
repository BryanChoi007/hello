import requests
import json
import time
import sys

tenant = "tenant1|2e1b962f-a0ec-49f0-8f01-d9c3f2095bd8"
data = tenant.split("|")
name= data[0]
print("Tenant: " + name)
id = data[1]
print("ID: " + id)

""""
from string import ascii_uppercase as alc
break_out_flag = False
#alpha = ["H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
alpha = ["K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
#alpha = ["S","T","U","V","W","X","Y","Z"]
#alpha = ["R","S","T","U","V","W","X","Y","Z"]
#alpha = ["U","V","W","X","Y","Z"]
for i in range(8,10):
    for j in alc:
        for k in alc:
            api_url = "https://licenseplatedata.com/consumer-api/SAMIR-LPDKV2F1Y/MD/" + str(i) + j + k + "6100"
            print(api_url)
            response = requests.get(api_url)
            print(response.content)
            if not response.content.startswith(b'<!DOCTYPE html>') and not response.content.startswith(b'<html>\n<head><title>500 Internal Server Error'):
                x = json.loads(response.content)
                if x["code"] != 404:
                    year = x["licensePlateLookup"]["year"]
                    make = x["licensePlateLookup"]["make"].upper()
                    model = x["licensePlateLookup"]["model"].upper()
                    print(year + " " + make + " " + model)
                    if make == 'TOYOTA' and model == 'TACOMA':
                        with open('vehicle.txt', 'a') as f:
                            print(str(i) + j + k + "6100" + " " + x["licensePlateLookup"]["name"] + " " + x["licensePlateLookup"]["vin"] + "\n", file=f)
                            #break_out_flag = True
                            #break
                time.sleep(2.6)
            #if break_out_flag:
                #break

        #if break_out_flag:
            #break       

#api_url = "https://licenseplatedata.com/consumer-api/BRYAN-LPDNL6CXN/TX/794S3S"
#response = requests.get(api_url)
#print(response.content)
#x = json.loads(response.content)
#print(x["licensePlateLookup"]["year"])
"""