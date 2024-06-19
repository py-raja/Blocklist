from ipaddress import ip_address

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
    return entry.replace("[", "").replace("]", "").replace("www.","").replace("http://","").replace("https://","")
        
def main():
    filename = input("Enter the path of the file containing IP addresses and FQDNs: ")
    entries = []
    with open(filename.strip('\"'), 'r') as file:
        for line in file:
            entry = line.strip()
            entry = remove_brackets(entry)
            entries.append(entry)

    print("config firewall address")
    for entry in entries:
        if is_valid_ip(entry):                
            print(generate_ip_address_config(entry))
        else:
            print(generate_fqdn_config(entry))
    print("end")

    print("config firewall addrgrp")
    print('edit "blocklist"')  # edit the Group name before execution
    for entry in entries:
        print(generate_addrgrp_config(entry))
    print("end")

if __name__ == "__main__":
    main()
