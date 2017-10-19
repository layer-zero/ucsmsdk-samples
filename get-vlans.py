#!/usr/bin/env python

"""Collect VLANs from a UCS and write them to a CSV file using the UCSM Python SDK"""

from getpass import getpass
from csv import writer
from ucsmsdk import ucshandle

default_ip = '192.168.218.182'
default_user = 'admin'
default_filename = 'sample-vlans-out.csv'

def get_parameters():
    ucsm_ip = raw_input('Target UCS IP address [{}]: '.format(default_ip)) or default_ip
    ucsm_user = raw_input('UCS user name [{}]: '.format(default_user)) or default_user
    ucsm_password = getpass('UCS password: ')
    csv_filename = raw_input('VLAN CSV file [{}]: '.format(default_filename)) or default_filename
    parameters = {'ip': ucsm_ip, 'user': ucsm_user, 'password': ucsm_password, 'filename': csv_filename}
    return parameters

def get_vlans(handle):
    filter_string = '(cloud, "ethlan", type="eq")'
    vlan_mos = handle.query_classid(class_id='fabricVlan', filter_str=filter_string)
    return vlan_mos

def write_vlans_to_csv(csv_filename, vlan_mos):
    with open(csv_filename,'wb') as vlan_file:
        vlan_csv = writer(vlan_file)
        vlan_csv.writerow(['id', 'name', 'fabric'])
        for vlan_mo in vlan_mos:
            if vlan_mo.switch_id == 'dual':
                print 'Adding global VLAN "{}" with id {} to file'.format(vlan_mo.name, vlan_mo.id)
            else:
                print 'Adding fabric {} VLAN "{}" with id {} to file'.format(vlan_mo.switch_id, vlan_mo.name, vlan_mo.id)               
            vlan_csv.writerow([vlan_mo.id, vlan_mo.name, vlan_mo.switch_id])

def main():
    ucs_params = get_parameters()
    handle = ucshandle.UcsHandle(ucs_params['ip'], ucs_params['user'], ucs_params['password'], secure=True)
    handle.login()
    vlans = get_vlans(handle)
    write_vlans_to_csv(ucs_params['filename'], vlans)
    handle.logout()

if __name__ == '__main__':
    main()