#!/usr/bin/env python

"""Import a UCS backup from file using the UCSM Python SDK"""

from ucsmsdk import ucshandle
from ucsmsdk.utils.ucsbackup import import_ucs_backup
from getpass import getpass

default_ip = '192.168.218.194'
default_user = 'admin'
default_filename = 'ucs-backup.xml'

def main():
    ucsm_ip = raw_input('Target UCS IP address [{}]: '.format(default_ip)) or default_ip
    ucsm_user = raw_input('UCS user name [{}]: '.format(default_user)) or default_user
    ucsm_password = getpass('UCS password: ')
    filename = raw_input('Filename for backup (in current directory) [{}]: '.format(default_filename)) or default_filename
    handle = ucshandle.UcsHandle(ucsm_ip, ucsm_user, ucsm_password, secure=True)
    handle.login()
    import_ucs_backup(handle, file_dir="./", file_name=filename)
    handle.logout()

if __name__ == '__main__':
    main()