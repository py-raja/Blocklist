# Fortigate Firewall Address Configuration Script

## Overview

This script is designed to automate the creation of firewall address configurations for both IP addresses and Fully Qualified Domain Names (FQDNs). The script reads a list of IP addresses and FQDNs from a specified file, generates the appropriate configuration commands, and prints them to the console or to a text file. It also eliminates unwanted characters,spaces and duplicates from inputs as shown below:

- `http://one.com` -> `one.com`
- `https://two.com` -> `two.com`
- `192[.]169[.]1[.]2` -> `192.169.1.2`
- `192[.]169[.]1[.]2` -> removed from output since it's duplicated
- `hxxp://three[.]com/xys` -> `three.com`
- `hxxp://three[.]com/sf` -> removed from output since it's duplicated
- `four[.]com` -> `four.com`
- `five.com` -> `five.com`
- `five.com` -> removed from output since it's duplicated

## Prerequisites

- Python 3.x
- A text file containing a list of IP addresses and FQDNs

## Usage

1. **Prepare the Input File:**
   - Create a text file containing a list of IP addresses and FQDNs.
   - Ensure each entry is on a separate line.
   - Example:
     ```
     192[.]168[.]1[.]1
     example[.]com
     [192.168.2.2]
     [www.test.com]
     https://example1.com/path
     https://example1.com/duplicate
     
     ```

2. **Run the Script:**
   (i) If the input files less entries and want to test the code via CLI use `blocklist_CLI.py` script
   
   - Save the script to a file, e.g., `blocklist_CLI.py`.
   - Execute the script in the terminal or command prompt:
     ```sh
     python blocklist_CLI.py
     ```
   - When prompted, enter the path to the input file:
     ```
     Enter the path of the file containing IP addresses and FQDNs: input.txt
     ```
   (ii) If the input files has N number of entries use `blocklist_file.py` script to save the output in text file
   
   - Save the script to a file, e.g., `blocklist_file.py`.
   - Execute the script in the terminal or command prompt:
     ```sh
     python blocklist_file.py
     ```
   - When prompted, enter the path to the input file:
     ```
     Enter the path of the file containing IP addresses and FQDNs: input.txt
     ```
     
4. **Output:**
   - The script will output the configuration commands to the CLI or in Text file.
   - Note : Output file will be saved in the name of current date_current time_output.txt('''20240727_122417_output.txt''')

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
edit "example1.com"
set type fqdn
set fqdn "example1.com"
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
append member example1.com
end
```

### Notes
Ensure the input file is properly formatted and accessible.
Edit the group name ("blocklist") in the address group configuration section as needed before executing the configuration commands on the firewall.
This script simplifies the process of creating firewall configurations, reducing manual effort and minimizing errors.
