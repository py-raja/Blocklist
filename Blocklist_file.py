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
    return entry.replace("[", "").replace("]", "").replace("www.","").replace("http://","").replace("https://","").replace("hxxps://","").replace("hxxp://","")
        
def main():
    input_filename = input("Enter the path of the file containing IP addresses and FQDNs: ")
    output_filename = input("Enter the path of the output file to write configurations: ")

    entries = []
    with open(input_filename.strip('\"'), 'r') as file:
        for line in file:
            entry = line.strip()
            entry = remove_brackets(entry)  # Remove [ and ] from entry
            entries.append(entry)

    with open(output_filename.strip('\"'), 'w') as output_file:
        output_file.write("config firewall address\n")
        for entry in entries:
            if is_valid_ip(entry):                
                output_file.write(generate_ip_address_config(entry) + "\n")
            else:
                output_file.write(generate_fqdn_config(entry) + "\n")
        output_file.write("end\n")

        output_file.write("config firewall addrgrp\n")
        output_file.write('edit "blocklist"\n')  # edit the Group name before execution
        for entry in entries:
            output_file.write(generate_addrgrp_config(entry) + "\n")
        output_file.write("end\n")

    print(f"Configurations have been written to {output_filename}")

if __name__ == "__main__":
    main()
