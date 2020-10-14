#!/usr/bin/env python
import requests
import pandas as pd
import tabulate
import json
pd.set_option('display.max_columns', 500)
import warnings
warnings.filterwarnings("ignore")
import sys, os
sys.path.append(os.getcwd())
from logs import *

def main():

    api_path = "https://sandboxsdwan.cisco.com:8443"

    requests.packages.urllib3.disable_warnings()

    # login_creds = {"j_username": "devnetuser", "j_password": "Cisco123!"}
    login_creds = {"j_username": "admin", "j_password": "C1sco12345"}

    sess = requests.session()
    auth_resp = sess.post(
        f"{api_path}/j_security_check", data=login_creds, verify=False
    )

    if not auth_resp.ok or auth_resp.text:
        print("Login failed")
        import sys
        sys.exit(1)

    device_resp = sess.get(f"{api_path}/dataservice/device", verify=False)
    if device_resp.ok:
        devices = device_resp.json()["data"]

        print(f"Devices managed by DevNet SD-WAN sandbox:")
        for dev in devices:
            print(f"Device IP: {dev['system-ip']:<12} Name: {dev['host-name']}")


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
        # print('successfully executed')
        response = device_resp.json()["data"]
    return response

def sdwan_get_list_of_device():
    col_of_interest = ['deviceId', 'system-ip', 'host-name', 'reachability', 'status', 'personality', 'uuid']
    # Get the list of Devices
    resp = execute_api_and_get_response('/dataservice/device')
    df = pd.DataFrame(resp)
    df = df[col_of_interest]
    log_info(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))
    return

def sdwan_get_dummy_call():
    df = pd.DataFrame(data = range(1,10))
    log_info(tabulate.tabulate(df, tablefmt='psql'))
    return

def sdwan_get_list_of_alarms():
    # Get the list of alarms
    resp = execute_api_and_get_response('/dataservice/alarms')
    log_info(f"{len(resp)} Total number of alarms found.")
    return

def sdwan_get_audit_logs():
    # Getting the audit logs
    resp = execute_api_and_get_response('/dataservice/auditlog')
    df = pd.DataFrame(resp)
    df = df.drop(['statcycletime', 'logusersrcip', 'auditdetails', 'tenant', 'logprocessid', 'logfeature'], axis = 1)
    df['logmessage'] = df['logmessage'].apply(lambda x: x[:45])
    log_info(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))
    return

def sdwan_get_alarm_count():
    # Get the alarm count
    resp = execute_api_and_get_response('/dataservice/alarms/count')
    df_alarm_count = pd.DataFrame(resp, index=[0])
    log_info(tabulate.tabulate(df_alarm_count, tablefmt='psql', headers = df_alarm_count.columns, showindex=False))
    return

def sdwan_get_connection_summary():
    # Connection summary
    resp = execute_api_and_get_response('/dataservice/network/connectionssummary')
    df = pd.DataFrame(resp)
    df = df.drop(['statusList'], axis = 1)
    log_info(tabulate.tabulate(df, tablefmt='psql', headers = df.columns, showindex=False))
    return

def sdwan_get_reboot_count():
    # Show reboot count
    resp = execute_api_and_get_response('/dataservice/network/issues/rebootcount')
    log_info(tabulate.tabulate(pd.DataFrame(resp, index=[0]), tablefmt='psql', headers = pd.DataFrame(resp, index=[0]).columns, showindex=False))
    return

def sdwan_get_device_status():
    # Show Device Monitor
    resp = execute_api_and_get_response('/dataservice/device/monitor')
    log_info(tabulate.tabulate(pd.DataFrame(resp), tablefmt='psql', headers = pd.DataFrame(resp).columns, showindex=False))
    return

def sdwan_show_vmanage_details():
    # server details
    resp = execute_api_and_get_response('/dataservice/client/server')
    log_info(json.dumps(resp, indent=2))
    return

def sdwan_show_connectivity_summary():
    # Site Health view
    resp = execute_api_and_get_response('/dataservice/device/bfd/sites/summary')[0]
    log_info(tabulate.tabulate(pd.DataFrame(resp), tablefmt='psql', headers = pd.DataFrame(resp).columns, showindex=False))
    return

def show_last_events():
    # Events summary ===> takes time to respond
    resp = execute_api_and_get_response('/dataservice/event/severity/summary')
    df_events_response = pd.DataFrame(resp)
    log_info(f'--- TOTAL NUM OF EVENTS FOUND : {df_events_response.shape[0]} -----')
    log_info('#==== SHOWING TOP 100 EVENTS === ')
    log_info(tabulate.tabulate(df_events_response.head(100), tablefmt='psql', headers = df_events_response.columns, showindex=False))
    return


if __name__ == "__main__":
    main()
