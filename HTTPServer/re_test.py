#!/usr/bin/env python3

import re


string = 'GET /admin.html HTTP/1.1'

pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'

# 返回一个字典，字典的键为捕获组的名字，值为匹配的字符串
env = re.match(pattern, string).groupdict()
print(env)
