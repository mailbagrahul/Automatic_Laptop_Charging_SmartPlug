# -*- coding: utf-8 -*-
# @Author: Raaghul Umapathy
# @Date:   2021-07-14 12:40:30
# @Last Modified by:   Raaghul Umapathy
# @Last Modified time: 2021-07-14 19:09:04

import urllib3
import json
import logging
import psutil
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def battery_level():
    logging.info('***Battery_Status***')
    battery = psutil.sensors_battery()  
    
    logging.info("Power plugged in : " + str(battery.power_plugged))
    logging.info("Battery percentage : " + str(battery.percent))
    
    return battery.power_plugged, battery.percent
  
def plug_handler(event):
    logging.info('***Smart Plug Handler***')
    logging.info('Received event: ')

    ##### Get the TP-Link RESTful API token 
    req = { "method": "login", "params": { "appType": "Kasa_Ios",  "cloudUserName": " ",  "cloudPassword": " ", "terminalUUID": " " }}
    req['params']['cloudUserName'] = os.environ.get("KASA_USERNAME")
    req['params']['cloudPassword'] = os.environ.get("KASA_PWD")
    req['params']['terminalUUID'] = os.environ.get("KASA_TERM_UUID")

    # Get Kasa API key - send POST to server and get response
    data = json.dumps(req).encode("utf-8")
    http = urllib3.PoolManager()
    response = http.request("POST", "https://wap.tplinkcloud.com", body=data, headers={'Content-Type': 'application/json'})
   
    
    rsp = json.loads(response.data.decode("utf-8"))["result"]
    
    apiToken = rsp['token']
    logging.info("Kasa API login response: " + str(rsp))

    ##### Get List of smart devices registered in Kasa(TP-link)
    req = { "method": "getDeviceList" }
    data = json.dumps(req).encode("utf-8")
    response = http.request("POST", "https://eu-wap.tplinkcloud.com/?token=" + apiToken, 
                        body=data, 
                        headers={'Content-Type': 'application/json'})
    
    rsp = json.loads(response.data.decode("utf-8"))
    logging.info("Kasa API get device list response: " + str(rsp))

    #  pick first device.     
    deviceId = rsp['result']['deviceList'][0]['deviceId']
    logging.info("Device selected: " + deviceId)


     # ON event by default
    req = {"method":"passthrough", "params": {"deviceId": " ", "requestData": "{\"system\":{\"set_relay_state\":{\"state\":1}}}" }}
    req['params']['deviceId'] = deviceId

    if event == 'on':
        logging.info('Turning switch ON')
    elif event == 'off':
        req['params']['requestData'] = "{\"system\":{\"set_relay_state\":{\"state\":0}}}"
        logging.info('Turning switch OFF')
    else:
        logging.info('Long press event not handled') # defaults to ON


    # Send HTTP POST indicating to turn the relay on or off
    data = json.dumps(req).encode("utf-8")
    response = http.request("POST", "https://use1-wap.tplinkcloud.com/?token=" + apiToken, 
                        body=data, 
                        )
    
    rsp = json.loads(response.data.decode("utf-8"))
    logging.info("Kasa API relay state change response: " + str(rsp))

# Check the status of the battery and trigger the event 
power_plugged, battery_percent = battery_level()
if battery_percent < 20 and power_plugged == False:
    plug_handler("on")
elif battery_percent == 100 and power_plugged == True:
    plug_handler("off")
else:
    logging.info("No worries")

logging.info("End")