# Firewall Address Configuration Script

## Overview

This script is designed to automate the creation of firewall address configurations for both IP addresses and Fully Qualified Domain Names (FQDNs). The script reads a list of IP addresses and FQDNs from a specified file, generates the appropriate configuration commands, and prints them to the console.

## Prerequisites

- Python 3.x
- A text file containing a list of IP addresses and FQDNs

## Usage

1. **Prepare the Input File:**
   - Create a text file containing a list of IP addresses and FQDNs.
   - Ensure each entry is on a separate line.
   - Example:
     ```
     192.168.1.1
     example.com
     [192.168.2.2]
     [www.test.com]
     ```

2. **Run the Script:**
   - Save the script to a file, e.g., `blocklist.py`.
   - Execute the script in the terminal or command prompt:
     ```sh
     python blocklist.py
     ```
   - When prompted, enter the path to the input file:
     ```
     Enter the path of the file containing IP addresses and FQDNs: input.txt
     ```

3. **Output:**
   - The script will output the configuration commands to the console.

## Example Output

### Firewall Address Configuration
```
config firewall address
edit "192.168.1.1"
set type ipmask
set subnet "192.168.1.1/32"
next
edit "example.com"
set type fqdn
set fqdn "example.com"
next
edit "192.168.2.2"
set type ipmask
set subnet "192.168.2.2/32"
next
edit "test.com"
set type fqdn
set fqdn "test.com"
next
end
```

### Firewall Address Group Configuration
```
config firewall addrgrp
edit "blocklist"
append member 192.168.1.1
append member example.com
append member 192.168.2.2
append member test.com
end
```

### Notes
Ensure the input file is properly formatted and accessible.
Edit the group name ("blocklist") in the address group configuration section as needed before executing the configuration commands on the firewall.
This script simplifies the process of creating firewall configurations, reducing manual effort and minimizing errors.
