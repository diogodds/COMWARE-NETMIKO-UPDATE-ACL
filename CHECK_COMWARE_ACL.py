#!/usr/bin/env python

from netmiko import ConnectHandler 
from datetime import datetime
import sys
import getpass
import re
 
 #######################################################################
 # Warnings module needed to be imported to solve a connection mode    #
 # deprecated warrning that I was geting when trying to connect to     #
 # the juniper switches                                                #
 #######################################################################

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

########################################################################

#timestr = time.strftime('%Y%m%d-%H%M%S')
#second_octect = raw_input('Please type the second octect of the supernet of the WH: ')

username = 'dsantos'
password = getpass.getpass()


########################################################################

#list_of_devices = ['10.191.255.61',
#                   '10.23.4.50',
#                  ]


#list_of_devices = open('COMWARE-DEVICES.txt','r')

with open('COMWARE-DEVICES.txt') as file: # This opens the text file with the name ARUBA-DEVICES.txt in csv format (IP,hostname)
    list_of_devices = file.read().splitlines() # The file is loaded into the "list_of_devices" variable and splited into lines

#######################################################################

for line in list_of_devices:
  host_to_cfg = line.split(',') #this will create a list by spliting the line into two elements, considering the coma as delimiter for the strip.
  #octects = host_to_create[0].split('.') 
  print('Establishing connection to ' + host_to_cfg[1])
  
  start_time = datetime.now()

  net_connect = ConnectHandler(device_type='hp_comware', ip=host_to_cfg[0], username=username, password=password, global_delay_factor=0.8)
  #net_connect = ConnectHandler(device_type='hp_procurve', ip=host_to_create[0], username=username, password=password)
  
  print('Connected to ' + host_to_cfg[1])
  
  net_connect.send_command('\n')
  acl = net_connect.send_command('display current-configuration | in ^acl.*2000', expect_string=r">").split(' ') # This gets the output of the command and create a list, we want to check if in the device the acl 200 is "nuber" or "basic"
  net_connect.send_command('system-view', expect_string=r"]") 
  net_connect.send_command('undo ssh server acl', expect_string=r"]")
  net_connect.send_command('undo acl ' + acl[1] + ' 2000', expect_string=r"]")
  net_connect.send_command('acl ' + acl[1] + ' 2000', expect_string=r"]")
  net_connect.send_command('description MGMT_ACCESS', expect_string=r"]")
  net_connect.send_command('rule 10 permit source 10.' + host_to_cfg[2] + '.221.0 0.0.0.255 counting', expect_string=r"]")
  net_connect.send_command('rule 10 comment WH_SERVER_VLAN', expect_string=r"]")
  net_connect.send_command('rule 20 permit source 10.' + host_to_cfg[2] + '.221.0 0.0.0.255 counting', expect_string=r"]")
  net_connect.send_command('rule 20 comment WH_MGMT_VLAN', expect_string=r"]")
  net_connect.send_command('rule 30 permit source 10.' + host_to_cfg[2] + '.96.0 0.0.0.255', expect_string=r"]")
  net_connect.send_command('rule 30 comment WH_IT_WIFI', expect_string=r"]")
  net_connect.send_command('rule 40 permit source 10.160.96.0 0.15.3.0', expect_string=r"]")
  net_connect.send_command('rule 40 comment IT_BNB_WIFI_SUBNETS', expect_string=r"]")
  net_connect.send_command('rule 50 permit source 10.162.96.0 0.0.3.255', expect_string=r"]")
  net_connect.send_command('rule 50 comment IT_BTDZ_WIFI_SUBNET', expect_string=r"]")
  net_connect.send_command('rule 60 permit source 10.166.96.0 0.0.3.255', expect_string=r"]")
  net_connect.send_command('rule 60 comment IT_BTDH_WIFI_SUBNET', expect_string=r"]")
  net_connect.send_command('rule 70 permit source 10.180.5.178 0', expect_string=r"]")
  net_connect.send_command('rule 70 comment CMK', expect_string=r"]")
  net_connect.send_command('rule 80 permit source 10.180.8.240 0.0.0.15', expect_string=r"]")
  net_connect.send_command('rule 80 comment NETBRAIN', expect_string=r"]")
  net_connect.send_command('rule 90 permit source 10.180.12.14 0.0.0.7', expect_string=r"]")
  net_connect.send_command('rule 90 comment LIBRE-NMS', expect_string=r"]")
  net_connect.send_command('rule 100 permit source 10.180.19.2 0', expect_string=r"]")
  net_connect.send_command('rule 100 comment IMC', expect_string=r"]")
  net_connect.send_command('rule 110 permit source 10.190.96.0 0.0.1.255', expect_string=r"]")
  net_connect.send_command('rule 110 comment VPN-CONNECTION-LOST', expect_string=r"]")
  net_connect.send_command('rule 120 permit source 10.190.80.0 0.0.15.255', expect_string=r"]")
  net_connect.send_command('rule 120 comment VPN-WHIT', expect_string=r"]")
  net_connect.send_command('rule 130 permit source 10.' + host_to_cfg[2] + '.4.0 0.0.0.255', expect_string=r"]")
  net_connect.send_command('rule 130 comment MGMT', expect_string=r"]")
  net_connect.send_command('rule 1000 deny logging', expect_string=r"]")
  net_connect.send_command('rule 1000 comment DENY_ANY_OTHER_TRAFFIC', expect_string=r"]")
  net_connect.send_command('ssh server acl 2000', expect_string=r"]")
  net_connect.send_command('save force', expect_string=r"]")
  
  end_time = datetime.now()
  
  print('\nConfiguration successfully applied to the device ' + host_to_cfg[1])
  print('Total time: {}'.format(end_time - start_time) +'\n' + '#' * 60)