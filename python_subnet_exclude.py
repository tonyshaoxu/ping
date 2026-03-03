
import ipaddress

# 192.168.0.0/16排除掉192.168.123.0/24

def exclude_subnet(base_network_str, exclude_network_str):
    base = ipaddress.ip_network(base_network_str)
    exclude = ipaddress.ip_network(exclude_network_str)
    
    # address_exclude returns an iterator of the remaining networks
    try:
        remaining_networks = list(base.address_exclude(exclude))
        # Sort them numerically for better readability
        remaining_networks.sort()
        return [str(net) for net in remaining_networks]
    except ValueError as e:
        # This happens if exclude is not part of base
        return [f"Error: {e}"]

if __name__ == "__main__":
    base_net = "192.168.0.0/16"
    exclude_net = "192.168.123.0/24"
    
    result = exclude_subnet(base_net, exclude_net)
    
    print(f"Networks in {base_net} excluding {exclude_net}:")
    for subnet in result:
        print(subnet)
