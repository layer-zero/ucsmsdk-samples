#!/usr/bin/env python

"""Make a UCS backup using the UCSM Python SDK"""

from ucsmsdk import ucshandle
from ucsmsdk.utils.ucsbackup import backup_ucs
from getpass import getpass

def main():
    ucsm_ip = raw_input('Target UCS IP address [https://192.168.218.165]: ') or '192.168.218.165'
    ucsm_user = raw_input('UCS user name [admin]: ') or 'admin'
    ucsm_password = getpass('UCS password: ')
    filename = raw_input('Filename for backup (in current directory) [ucs_backup.xml]: ') or 'ucs_backup.xml'
    handle = ucshandle.UcsHandle(ucsm_ip, ucsm_user, ucsm_password, secure=True)
    handle.login()
    backup_ucs(handle, backup_type="config-all", file_dir="./", file_name=filename)
    handle.logout()

if __name__ == '__main__':
    main()