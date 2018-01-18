#!/usr/bin/env python

"""Create VLANs from a CSV file using the UCSM Python SDK"""

from getpass import getpass
from csv import reader
from ucsmsdk import ucshandle
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan

default_ip = '192.168.218.194'
default_user = 'admin'
default_filename = 'sample-vlans-in.csv'

def get_parameters():
    ucsm_ip = raw_input('Target UCS IP address [{}]: '.format(default_ip)) or default_ip
    ucsm_user = raw_input('UCS user name [{}]: '.format(default_user)) or default_user
    ucsm_password = getpass('UCS password: ')
    csv_filename = raw_input('VLAN CSV file [{}]: '.format(default_filename)) or default_filename
    parameters = {'ip': ucsm_ip, 'user': ucsm_user, 'password': ucsm_password, 'filename': csv_filename}
    return parameters

def extract_vlans_from_csv(csv_filename):
    with open(csv_filename,'rb') as vlan_file:
        vlans = []
        vlan_csv = reader(vlan_file)
        first_row = True
        for row in vlan_csv:
            if first_row:
                header = row
                first_row = False
            else:
                colnum = 0
                vlan = {}
                for field in row:
                    if header[colnum] == 'id':
                        vlan['id'] = field
                    elif header[colnum] == 'name':
                        vlan['name'] = field
                    colnum += 1
                vlans.append(vlan)
    return vlans        

def vlan_exists(handle, vlan_name):
    vlan_dn = 'fabric/lan/net-{}'.format(vlan_name)
    vlan = handle.query_dn(vlan_dn)
    if vlan is not None:
        return True
    else:
        return False

def create_vlan(handle, vlan_name, vlan_id):
    vlan_mo = FabricVlan(parent_mo_or_dn='fabric/lan', name=vlan_name, id=vlan_id)
    handle.add_mo(vlan_mo)
    handle.commit()

def main():
    ucs_params = get_parameters()
    vlans = extract_vlans_from_csv(ucs_params['filename'])
    handle = ucshandle.UcsHandle(ucs_params['ip'], ucs_params['user'], ucs_params['password'], secure=True)
    handle.login()
    for vlan in vlans:
        if not vlan_exists(handle, vlan['name']):
            print 'Creating VLAN {} with VLAN id {}'.format(vlan['name'], vlan['id'])
            create_vlan(handle, vlan['name'], vlan['id'])
        else:
            print 'A VLAN with name {} already exists'.format(vlan['name'])
    handle.logout()

if __name__ == '__main__':
    main()