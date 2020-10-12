#!/usr/bin/env python

import requests
import pandas as pd
import tabulate
import json
pd.set_option('display.max_columns', 500)
import warnings
warnings.filterwarnings("ignore")
import sys, os
from pathlib import Path
sys.path.append(Path(os.getcwd()).parent)
from logs import *

def main():
    """
    Execution begins here.
    """

    # Basic variables to reduce typing later. The API path is just the
    # always-on SD-WAN API (really, vManage) sandbox in DevNet.
    # IMPORTANT: You can see the full list of API calls using on-box
    # API documentation here: https://sandboxsdwan.cisco.com:8443/apidocs
    api_path = "https://sandboxsdwan.cisco.com:8443"

    # The SD-WAN sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # These credentials are supplied by Cisco DevNet on the sandbox page.
    # These specific parameters may change, so be sure to check here:
    # https://developer.cisco.com/sdwan/learn/
    # login_creds = {"j_username": "devnetuser", "j_password": "Cisco123!"}
    login_creds = {"j_username": "admin", "j_password": "C1sco12345"}

    # Create a single TCP session to the SD-WAN sandbox. This allows the cookies
    # and other state to be re-used without having to manually pass tokens around.
    # We can perform regular HTTP requests on this "sess" object now.
    sess = requests.session()
    auth_resp = sess.post(
        f"{api_path}/j_security_check", data=login_creds, verify=False
    )

    # An authentication request has failed if we receive a failing return code
    # OR if there is any text supplied in the response. Failing authentications
    # often return code 200 (OK) but include a lot of HTML content, indicating a
    # a failure. If a failure does occur, exit the program using code 1.
    if not auth_resp.ok or auth_resp.text:
        print("Login failed")
        import sys
        sys.exit(1)

    # At this point, we've authenticated to SD-WAN using the REST API and can
    # issue follow-on requests. Next, we collect a list of devices. Assuming
    # the request worked, iterate over the list of devices and print out
    # the device IP address and hostname for each device.
    device_resp = sess.get(f"{api_path}/dataservice/device", verify=False)
    if device_resp.ok:
        devices = device_resp.json()["data"]

        # Debugging line; pretty-print JSON to see structure
        # import json; print(json.dumps(devices, indent=2))

        print(f"Devices managed by DevNet SD-WAN sandbox:")
        for dev in devices:
            print(f"Device IP: {dev['system-ip']:<12} Name: {dev['host-name']}")


        # Printing Data in DataFrame format
        print(pd.DataFrame.from_dict(device_resp.json()["data"]))

def execute_api_and_get_response(api_path_rest):
    response = None
    api_path = "https://10.10.20.90:8443"
    # login_creds = {"j_username": "devnetuser", "j_password": "Cisco123!"}
    login_creds = {"j_username": "admin", "j_password": "C1sco12345"}

    sess = requests.session()
    auth_resp = sess.post(
        f"{api_path}/j_security_check", data=login_creds, verify=False
    )

    # device_resp = sess.get(f"{api_path}/dataservice/device", verify=False)
    device_resp = sess.get(f"{api_path}{api_path_rest}", verify=False)
    if device_resp.ok:
        print('successfully executed')
        response = device_resp.json()["data"]

    return response

def sdwan_get_list_of_device():
    col_of_interest = ['deviceId', 'system-ip', 'host-name', 'reachability', 'status', 'personality', 'uuid']
    # Get the list of Devices
    resp = execute_api_and_get_response('/dataservice/device')
    df = pd.DataFrame(resp)
    df = df[col_of_interest]
    print(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))
    return

def sdwan_get_dummy_call():
    df = pd.DataFrame(data = range(1,10))
    print(tabulate.tabulate(df, tablefmt='psql'))
    return

def sdwan_get_list_of_alarms():
    # Get the list of alarms
    execute_api_and_get_response('/dataservice/alarms')
    return

def sdwan_get_audit_logs():
    # Getting the audit logs
    resp = execute_api_and_get_response('/dataservice/auditlog')
    df = pd.DataFrame(resp)
    df = df.drop(['statcycletime', 'logusersrcip', 'auditdetails', 'tenant', 'logprocessid', 'logfeature'], axis = 1)
    print(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))
    return

def sdwan_get_alarm_count():
    # Get the alarm count
    resp = execute_api_and_get_response('/dataservice/alarms/count')
    df_alarm_count = pd.DataFrame(resp, index=[0])
    print(tabulate.tabulate(df_alarm_count, tablefmt='psql', headers = df_alarm_count.columns, showindex=False))
    return

def sdwan_get_connection_summary():
    # Connection summary
    resp = execute_api_and_get_response('/dataservice/network/connectionssummary')
    df = pd.DataFrame(resp)
    df = df.drop(['statusList'], axis = 1)
    print(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))

def sdwan_get_reboot_count():
    # Show reboot count
    resp = execute_api_and_get_response('/dataservice/network/issues/rebootcount')
    print(tabulate.tabulate(pd.DataFrame(resp, index=[0]), tablefmt='psql', headers = pd.DataFrame(resp, index=[0]).columns, showindex=False))
    return

if __name__ == "__main__":
    main()

    # # Get the list of Devices
    # resp = execute_api_and_get_response('/dataservice/device')[0]
    # print(tabulate.tabulate(pd.DataFrame(resp), tablefmt='psql', headers = pd.DataFrame(resp).columns, showindex=False))

    # # Get the list of alarms
    # execute_api_and_get_response('/dataservice/alarms')

    # # Getting the audit logs
    # resp = execute_api_and_get_response('/dataservice/auditlog')
    # df_audit = pd.DataFrame.from_dict(resp)
    # print(tabulate.tabulate(df_audit, tablefmt='psql', headers = df_audit.columns, showindex=False))

    # # Get the alarm count
    # resp = execute_api_and_get_response('/dataservice/alarms/count')
    # df_alarm_count = pd.DataFrame(resp, index=[0])
    # print(tabulate.tabulate(df_alarm_count, tablefmt='psql', headers = df_alarm_count.columns, showindex=False))

    # # Connection summary
    # resp = execute_api_and_get_response('/dataservice/network/connectionssummary')
    # print(tabulate.tabulate(pd.DataFrame(resp), tablefmt='psql', headers = pd.DataFrame(resp).columns, showindex=False))

    # Show reboot count
    resp = execute_api_and_get_response('/dataservice/network/issues/rebootcount')
    print(tabulate.tabulate(pd.DataFrame(resp, index=[0]), tablefmt='psql', headers = pd.DataFrame(resp, index=[0]).columns, showindex=False))

    # Show Device Monitor
    resp = execute_api_and_get_response('/dataservice/device/monitor')[0]
    print(tabulate.tabulate(pd.DataFrame(resp, index=[0]), tablefmt='psql', headers = pd.DataFrame(resp, index=[0]).columns, showindex=False))


    # server details
    resp = execute_api_and_get_response('/dataservice/client/server')
    print(json.dumps(resp, indent=2))

    # Site Health view
    resp = execute_api_and_get_response('/dataservice/device/bfd/sites/summary')[0]
    print(tabulate.tabulate(pd.DataFrame(resp), tablefmt='psql', headers = pd.DataFrame(resp).columns, showindex=False))

    # Events summary ===> takes time to respond
    resp = execute_api_and_get_response('/dataservice/event/severity/summary')
    df_events_response = pd.DataFrame(resp)
    print(f'--- TOTAL NUM OF EVENTS FOUND : {df_events_response.shape[0]} -----')
    print('#==== SHOWING TOP 100 EVENTS === ')
    print(tabulate.tabulate(df_events_response.head(100), tablefmt='psql', headers = df_events_response.columns, showindex=False))

    # Ping a Device ID
