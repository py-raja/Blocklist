from ipaddress import ip_address
from urllib.parse import urlparse
import re

def is_valid_ip(ip):
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False

def generate_ip_address_config(ip):
    return f"""edit "{ip}"
    set type ipmask
    set subnet "{ip}/32"
next"""

def generate_fqdn_config(fqdn):
    return f"""edit "{fqdn}"
    set type fqdn
    set fqdn "{fqdn}"
next"""

def generate_addrgrp_config(entry):
    return f"""   append member {entry}"""

def remove_brackets(entry):
    return entry.replace("[", "").replace("]", "").replace("www.","https://").replace("http://","https://").replace("https://","https://").replace("hxxps://","https://").replace("hxxp://","https://")
        
def main():
    filename = input("Enter the path of the file containing IP addresses and FQDNs: ")
    url_pattern = re.compile(r"https?://[^\s'\"]+")
    entries = set()
    ips = set()
    domains = set()
    
    with open(filename.strip('\"'), 'r') as file:
        for line in file:
            entry = line.strip()
            entry = remove_brackets(entry)  # Remove brackets and change to https
            entries.add(entry)
    
    print("config firewall address")
    for entry in entries:
        if is_valid_ip(entry):                
            print(generate_ip_address_config(entry))
            ips.add(entry)
        elif re.match(url_pattern, entry):
            parsed_url = urlparse(entry.strip())
            domain = parsed_url.hostname
            if domain and domain not in domains:
                print(generate_fqdn_config(domain))
                domains.add(domain)
        else:
            if entry not in domains:
                print(generate_fqdn_config(entry))
                domains.add(entry)

    print("end")

    print("config firewall addrgrp")
    print('edit "blocklist"')  # Edit the group name before execution
    for ip in ips:
        print(generate_addrgrp_config(ip))
    for domain in domains:
        print(generate_addrgrp_config(domain))
    print("end")

if __name__ == "__main__":
    main()
