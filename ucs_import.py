#!/usr/bin/env python

"""Import a UCS backup from file using the UCSM Python SDK"""

from ucsmsdk import ucshandle
from ucsmsdk.utils.ucsbackup import import_ucs_backup
from getpass import getpass

def main():
    ucsm_ip = raw_input('Target UCS IP address [https://192.168.218.182]: ') or '192.168.218.182'
    ucsm_user = raw_input('UCS user name [admin]: ') or 'admin'
    ucsm_password = getpass('UCS password: ')
    filename = raw_input('Filename for backup (in current directory) [ucs_backup.xml]: ') or 'ucs_backup.xml'
    handle = ucshandle.UcsHandle(ucsm_ip, ucsm_user, ucsm_password, secure=True)
    handle.login()
    import_ucs_backup(handle, file_dir="./", file_name=filename)
    handle.logout()

if __name__ == '__main__':
    main()