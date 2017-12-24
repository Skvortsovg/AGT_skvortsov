import json
import requests

import os
import sys
sys.path.insert(0,'..')


publics_list = open('../config/config.json').read()
publics_list = json.loads(publics_list)


members = requests.post('http://api.vk.com/method/groups.getMembers',
                        data={'group_id':str(publics_list['public_id'][0])}).json()
count_members = members['response']['count']
exit(str(count_members))


