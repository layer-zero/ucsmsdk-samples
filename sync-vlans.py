#!/usr/bin/env python

"""Sync VLANs from a source UCS to a target UCS using the UCSM Python SDK"""

from getpass import getpass
from ucsmsdk import ucshandle
from ucsmsdk.utils import comparesyncmo

default_src_ip = '192.168.218.194'
default_dst_ip = '192.168.218.197'
default_username = 'admin'

def get_parameters(location, default_ip, default_user):
    ucsm_ip = raw_input('{} UCS IP address [{}]: '.format(location, default_ip)) or default_ip
    ucsm_user = raw_input('UCS user name [{}]: '.format(default_user)) or default_user
    ucsm_password = getpass('UCS password: ')
    parameters = {'ip': ucsm_ip, 'user': ucsm_user, 'password': ucsm_password}
    return parameters

def get_vlans(handle):
    filter_string = '(cloud, "ethlan", type="eq")'
    vlan_mos = handle.query_classid(class_id='fabricVlan', filter_str=filter_string)
    return vlan_mos


def main():
    src_ucs_params = get_parameters('Source', default_src_ip, default_username)
    dst_ucs_params = get_parameters('Destination', default_dst_ip, default_username)
    src_handle = ucshandle.UcsHandle(src_ucs_params['ip'], src_ucs_params['user'], src_ucs_params['password'], secure=True)
    dst_handle = ucshandle.UcsHandle(dst_ucs_params['ip'], dst_ucs_params['user'], dst_ucs_params['password'], secure=True)
    src_handle.login()
    dst_handle.login()
    src_vlans = get_vlans(src_handle)
    dst_vlans = get_vlans(dst_handle)
    diff_vlans = comparesyncmo.compare_ucs_mo(dst_vlans, src_vlans)
    if diff_vlans:
        print 'Followin VLANs will be synced:\n'
        comparesyncmo.write_mo_diff(diff_vlans)
        print '\nSyncing VLANs...\n'
        comparesyncmo.sync_ucs_mo(dst_handle, diff_vlans, delete_not_present=True)
    else:
        print 'VLANs are already in sync.'
    src_handle.logout()
    dst_handle.logout()

if __name__ == '__main__':
    main()