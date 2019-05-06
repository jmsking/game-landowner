#! /usr/bin/env python3

import datetime
import time

objs = [
    {
      "state": "constant.JOB_STATE_ERROR",
      "create_date": "2019-03-29",
      "task_num": 1
    },
    {
      "state": "constant.JOB_STATE_ERROR",
      "create_date": "2019-04-09",
      "task_num": 1
    },
    {
      "state": "creating",
      "create_date": "2019-04-09",
      "task_num": 1
    }
  ]
ans = dict()
ans['constant.JOB_STATE_VALIDATED'] = list()
ans['constant.JOB_STATE_COMPLETED'] = list()
ans['constant.JOB_STATE_ERROR'] = list()
ans['constant.MODELS_LIST_STATE_ALL'] = list()
has_date = dict()
has_date['constant.JOB_STATE_VALIDATED'] = list()
has_date['constant.JOB_STATE_COMPLETED'] = list()
has_date['constant.JOB_STATE_ERROR'] = list()
has_date['constant.MODELS_LIST_STATE_ALL'] = list()
date_dict = dict()
for item in objs:
    state = item.get('state', 'all')
    create_date = item.get('create_date', '1970-01-01')
    task_num = item.get('task_num', 0)
    if state in ans:
        ans[state].append({'create_date':create_date,'task_num':task_num})
        has_date[state].append(create_date)
    if create_date not in date_dict:
        date_dict[create_date] = task_num
    else:
        date_dict[create_date] += task_num
created_state_key = 'constant.MODELS_LIST_STATE_ALL'
for key, value in date_dict.items():
    if created_state_key not in ans:
        ans[created_state_key] = list()
    ans[created_state_key].append({'create_date':key, 'task_num': value})
    has_date[created_state_key].append(key)
s_time = datetime.datetime.strptime('2019-03-20', '%Y-%m-%d')
e_time = datetime.datetime.strptime('2019-04-15', '%Y-%m-%d')
while s_time <= e_time:
    for item_date in has_date:
        s_time_str = s_time.strftime('%Y-%m-%d')
        if s_time_str not in has_date[item_date]:
            ans[item_date].append({'create_date':s_time_str,'task_num':0})
    s_time += datetime.timedelta(days=1)
res = dict()
for key in ans:
    ans_state = ans.get(key,[])
    ans_state = sorted(ans_state, key=lambda x:x['create_date'])
    res[key] = ans_state
del date_dict, ans

#print(res)
import numpy as np
arr = np.array([7,1], dtype=np.float32)
print(arr.shape)
print(arr)
arr = np.column_stack((arr,arr,arr))
print(arr.shape)
print(arr)