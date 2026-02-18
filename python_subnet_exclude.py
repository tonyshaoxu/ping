
import ipaddress

# 192.168.0.0/16排除掉192.168.123.0/24

def exclude_subnet(base_network, exclude_network):
    base = ipaddress.ip_network(base_network)
    exclude = ipaddress.ip_network(exclude_network)
    
    # 计算排除后的子网
    result = []
    for subnet in base.subnets():
        if not exclude.overlaps(subnet):
            result.append(str(subnet))
        elif subnet.overlaps(exclude):
            # 如果子网与排除的子网重叠，则进一步细分
            for sub in subnet.subnets():
                if not exclude.overlaps(sub):
                    result.append(str(sub))
    return result

if __name__ == "__main__":
    base_network = "192.168.0.0/16"
    exclude_network = "192.168.123.0/24"
    result = exclude_subnet(base_network, exclude_network)
    for subnet in result:
        print(subnet)
