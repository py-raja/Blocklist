from ipaddress import ip_address
from urllib.parse import urlparse
import re
from datetime import datetime
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
    return entry.replace("[", "").replace("]", "").replace("http://www.","https://").replace("https://www.","https://").replace("www.","https://").replace("http://","https://").replace("https://","https://").replace("hxxps://","https://").replace("hxxp://","https://")

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
    
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{current_datetime}_output.txt"
    
    with open(output_filename, 'w') as output_file:
        output_file.write("config firewall address\n")
        for entry in entries:
            if is_valid_ip(entry):                
                output_file.write(generate_ip_address_config(entry) + '\n')
                ips.add(entry)
            elif re.match(url_pattern, entry):
                parsed_url = urlparse(entry.strip())
                domain = parsed_url.hostname
                if domain and domain not in domains:
                    output_file.write(generate_fqdn_config(domain) + '\n')
                    domains.add(domain)
            else:
                if entry not in domains:
                    output_file.write(generate_fqdn_config(entry) + '\n')
                    domains.add(entry)
        
        output_file.write("end\n")
        
        output_file.write("config firewall addrgrp\n")
        output_file.write('edit "blocklist"\n')  # Edit the group name before execution
        for ip in ips:
            output_file.write(generate_addrgrp_config(ip) + '\n')
        for domain in domains:
            output_file.write(generate_addrgrp_config(domain) + '\n')
        output_file.write("end\n")

    print(f"Output written to {output_filename}")

if __name__ == "__main__":
    main()
