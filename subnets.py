#!/usr/bin/python3

from ipaddress import ip_network

start = '0.0.0.0/0'
#需要排除的ip或者ip段
exclude = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '6.6.6.6', '8.8.8.8']

result = [ip_network(start)]
for x in exclude:
    n = ip_network(x)
    new = []
    for y in result:
        if y.overlaps(n):
            new.extend(y.address_exclude(n))
        else:
            new.append(y)
    result = new

print(','.join(str(x) for x in sorted(result)))
