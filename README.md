# Automatic Laptop Charging thru TP-Link SmartPlug
This program directly connects and controls your TP-Link power plug (smart home power switch) by checking your battery status. For more convenient and to check the status every 5 or 10 minutes, trigger this program thru windows task scheduler.

## Description

The motivation for this project was the fact that we leave our laptop charger connected 24/7 which leads to over heating and reducing battery life. Although you can control the HS110 power switch using the Kasa mobile app supported by TP-Link, it is not really convenient to have to use your phone to switch the power switch on and off. 

Note that the project uses a 3rd party (TP-Link) web API to communicate with the HS110. This API might change without notice in which case this function might stop working and would need to be updated accordingly.

## Setup

- Create a Kasa account from the Kasa mobile App
- Log into the app and register your TP-Link HS110 in it. Note that the HS110 has to be plugged in and able to connect to your WiFi network at the time it's being set up. If you do it correctly, you'll be able to turn the HS110 switch on and off from within the app.
- Set your Kasa/TP-Link credentials 
  - set KASA_USERNAME, KASA_PWD, KASA_TERM_UUID as environment variables in your machine
  - Generate an UUID using https://www.uuidgenerator.net/version4 and set KASA_TERM_UUID in above step
- Schedule this program every N minutes to check the battery status and control the smart plug to turn on/off the laptop charger.
