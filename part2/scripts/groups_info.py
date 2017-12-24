#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import urllib
import json
from time import sleep
from datetime import datetime, timedelta
import os
import sys
sys.path.insert(0,'..')

from cfg import access_token
import requests


def get_json(url):
    getjson = urllib.request.urlopen(url).read().decode('utf-8')
    getjson = json.loads(getjson)
    sleep(0.3)
    return getjson

count_downloaded = 0

publics_list = open('../config/config.json').read()
publics_list = json.loads(publics_list)

fout = open('../tmp/groups_' + str(publics_list['public_id'][0]) + '.csv', 'w')
csvwriter = csv.writer(fout)
csvwriter.writerows([['id','name','description','count_members', 'count_posts', 'count_members']])
users=[]


offset = 0
print('Listing users...')
members = requests.post('https://api.vk.com/method/groups.getMembers?fields=name', data={'access_token': access_token,
                                                                                                      'count': 1,
                                                                                                      'offset': offset,
                                                                                                      'group_id': str(publics_list['public_id'][0])}
                        ).json()

if ('response' in members):
    members_count = members['response']['count']
while True:
    members = requests.post('https://api.vk.com/method/groups.getMembers?fields=name,sex,bdate,city,universities',
                            data={'access_token': access_token,
                                  'count': 1000,
                                  'offset': offset,
                                  'group_id': str(publics_list['public_id'][0])}
                            ).json()
    offset += 1000

group_list = {}
curr_user = 1
print(users)

for user in users:
    groups_processed = 0
    try:
        groups = requests.post('https://api.vk.com/method/groups.get',
                               data={'access_token': access_token,
                                     'count': 1000,
                                     'offset': offset,
                                     'extended': 1,
                                     'user_id': str(user)}).json()
    except:
        print ('Failed getting id' + str(user) + "' groups")
    if ('response' in groups):
        print('Processing user '+ str(curr_user)+ ' out of '+str(len(users))+"...")

        curr_user += 1

        del groups['response'][0]
        for group in groups['response']:
            groups_processed += 1
            if (group['gid'] not in group_list):

                count_downloaded += 1
                if (count_downloaded % 25 == 0):
                    fout.close()
                    fout = open('../tmp/groups_' + str(publics_list['public_id'][0]) + '.csv', 'a')
                    csvwriter = csv.writer(fout)

                print ('Processing group №' + str(groups_processed) + ' out of ' + str(len(groups['response'])))
                wall = 'https://api.vk.com/method/wall.get?access_token=' + access_token + '&filter=owner&offset=0&count=1&owner_id=-' + str(group['gid'])
                try:
                    wall = get_json(wall)
                except:
                    print ('Failed getting ' + str(group['gid']) + ' wall')
                if 'response' in wall:
                    count_posts = wall['response'][0]

                group_list[group['gid']] = 1
                group_info = 'https://api.vk.com/method/groups.getById?group_id=' + str(group['gid']) + '&fields=description,members_count'
                try:
                    group_info = get_json(group_info)
                except:
                    print ('Failed getting ' + str(group['gid']) + ' info')
                if ('response' in group_info):
                    for group in group_info['response']:
                        description = ''
                        members_count = 0
                        name = ''
                        if ('name' in group):
                            name = group['name']
                            name = name.replace(';', ':')
                        if ('description' in group):
                            description = group['description']
                            description = description.replace(';', ':')
                        if ('members_count' in group):
                            members_count = group['members_count']
                        csvwriter.writerows([[group['gid'], name, description, str(members_count), count_posts]])
            else:
                group_list[group['gid']] += 1

fout.close()
fout = open('../tmp/groups_' + str(publics_list['public_id'][0]) + '.csv', 'r')
info = open('../results/csv/groups_' + str(publics_list['public_id'][0]) + '.csv', 'w')
csvreader = csv.reader(fout)
csvwriter = csv.writer(info)
csvwriter.writerows([['id','name','description','count_members', 'count_posts', 'count_members']])
next(csvreader)
for row in csvreader:
    csvwriter.writerows([[row[0], row[1], row[2], row[3], row[4], group_list[int(row[0])]]])

fout.close()
info.close()

#os.remove('../tmp/groups_' + str(publics_list['public_id'][0]) + '.csv')