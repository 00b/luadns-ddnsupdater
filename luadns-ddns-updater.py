#!/usr/bin/python3
import requests
import json

#API documentation https://luadns.com/api.html

user_id = 'email@tld.com'
api_key = 'abc123xyz890'

target_zone_name = 'zone.tld'
target_record_name = 'hostname.zone.tld'
target_type = 'A'
target_ttl = '3600'

dns_api_base_url = 'https://api.luadns.com/v1'

def get_internetip():
    ip_url = 'https://ipv4.jsonip.com/'
    response = requests.get(ip_url)
    data = json.loads(response.content)
    return(data['ip'])

def get_zones():
    req_url = dns_api_base_url + '/zones'  
    response = requests.get(req_url, auth=(user_id,api_key), headers={'Accept': 'application/json'})
    data = json.loads(response.content)
    return (data)

def find_zone_id(zonename):
    zones = get_zones()
    for i in zones:
        if i['name']==zonename:
            zoneid = i['id']
        return(i['id'])

def get_zone_records(zone_id):
    req_url = dns_api_base_url + '/zones/'+str(zone_id)
    response = requests.get(req_url, auth=(user_id,api_key), headers={'Accept': 'application/json'})
    data = json.loads(response.content)
    return(data)

def find_record_id(record_name,record_type,zone_id):
    if not record_name.endswith('.'):
        record_name = record_name+'.'
    data = get_zone_records(zone_id)
    for i in data['records']:
        if i['name'] == record_name and i['type'] == record_type:
            return(i['id'])

def get_record_data(record_name,record_type,record_zone):
    zone_id = find_zone_id(record_zone)
    record_id = find_record_id(record_name,record_type,zone_id)
    req_url = dns_api_base_url + '/zones/'+str(zone_id)+'/records/'+str(record_id)
    response = requests.get(req_url, auth=(user_id,api_key), headers={'Accept': 'application/json'})
    data = json.loads(response.content)
    return(data)

def update_record(record_name,record_type,record_content,zone_name,record_ttl=3600):
    zone_id = find_zone_id(zone_name)
    record_id = find_record_id(record_name,record_type,zone_id)
    if record_name == zone_name:
        record_name == '@'+zone_name+'.'
    #make sure we have the dot at the end of the hostname for a super complete fqdn.
    if not record_name.endswith('.'):
        record_name = record_name+'.'
    req_url = dns_api_base_url +'/zones/'+str(zone_id)+'/records/'+str(record_id)
    update_data = {'zone_id':zone_id,'id':record_id,'name':record_name,'type':record_type,'content':record_content,'ttl':record_ttl}
    json_data = json.dumps(update_data)
    response = requests.put(req_url, auth=(user_id,api_key),headers={'Accept': 'application/json'},data=json_data)
    data = json.loads(response.content)
    return(data)

#Get internet wan IP. 
wan_internet_ip = get_internetip()
#print('Internet IP: '+wan_internet_ip)

#Get what lua dns record info for the target_record_name.  
dns_record_data = get_record_data(target_record_name,target_type,target_zone_name)
#print('DNS A record for '+target_record_name+': '+dns_record_data['content'])

#if the internet IP doesn't match the DNS record IP. Update the DNS record IP. 
if dns_record_data['content'] != wan_internet_ip:
    #print('Internet IP does not match record content. Updating DNS record')
    update_record(target_record_name,target_type,wan_internet_ip,target_zone_name)
