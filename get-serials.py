#!/usr/bin/env python

"""Collect serial numbers from a UCS using the UCSM Python SDK"""

from getpass import getpass
from ucsmsdk import ucshandle

default_ip = '192.168.218.194'
default_user = 'admin'

def get_parameters():
    ucsm_ip = raw_input('Target UCS IP address [{}]: '.format(default_ip)) or default_ip
    ucsm_user = raw_input('UCS user name [{}]: '.format(default_user)) or default_user
    ucsm_password = getpass('UCS password: ')
    parameters = {'ip': ucsm_ip, 'user': ucsm_user, 'password': ucsm_password}
    return parameters

def get_chassis(handle):
    chassis_mos = handle.query_classid(class_id='equipmentChassis')
    return chassis_mos

def get_blades(handle):
    filter_string = '(presence, "equipped", type="eq")'
    blade_mos = handle.query_classid(class_id='fabricComputeSlotEp', filter_str=filter_string)
    return blade_mos

def get_rackservers(handle):
    rackserver_mos = handle.query_classid(class_id='computeRackUnit')
    return rackserver_mos

def main():
    ucs_params = get_parameters()
    handle = ucshandle.UcsHandle(ucs_params['ip'], ucs_params['user'], ucs_params['password'], secure=True)
    handle.login()
    chassis_list = get_chassis(handle)
    blade_list = get_blades(handle)
    rackserver_list = get_rackservers(handle)
    print '\n{0:12} {1:12}'.format('Chassis','Serial number')
    for chassis in chassis_list:
    	print '{0:12} {1:12}'.format(chassis.id, chassis.serial)
    print '\n{0:12} {1:12}'.format('Blade','Serial number')
    for blade in blade_list:
	   	print '{0:12} {1:12}'.format(blade.chassis_id+'/'+blade.slot_id, blade.serial)
    print '\n{0:12} {1:12}'.format('Rack Server','Serial number')
    for rackserver in rackserver_list:
    	print '{0:12} {1:12}'.format(rackserver.id, rackserver.serial)
    handle.logout()

if __name__ == '__main__':
    main()
