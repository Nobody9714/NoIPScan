## Summary

NoIPScan is a Python script designed to scan your local network for connected devices. I made this python script so there is an IP scanner option that is not full of bloatware, spyware, ads, data harvesting, or fake download links like you'll find on most websites. This tool was developed with the assistance of Claude 3.5 Sonnet and other genorative AI models for images.

## Features

- Fast and efficient IP scanning
- Automatic detection of local IP range
- Concurrent scanning for improved speed
- Various means to help identify devices other than using IP/MAC addresses.
- Alphanumaricly sortable list by clicking the headers or right clicking in the list > sort > sorting option.
- Disable MAC address lookup using https://api.macvendors.com. This will slightly increase scan speed but also make it harder to identify what the devices are.
  
## How to Use

Easy Methode: 

1. Double click the file called "NoIpScan.bat".
   
2. Agree to install any missing dependencies.
   
3. Everything in the program should be fine to leave as default. Just press the "Scan Network" button to scan for devices on your local network.

   ![program](https://github.com/user-attachments/assets/eaadccf0-22a5-4730-959a-a7b35c690312)

   Optional:
   
   a. Custom network address.
   
   b. Custom IP range from 1-254
   
   c. Hide MAC Address, toggle to hide/unhide all mac addresses.
   
   d. Disable MAC Address lookup on https://api.macvendors.com. This is encase you dont want to use this to help identify devices more thoroughly than just IP and MAC addresses.

   e. # of scans to do on the network because sometimes 1 isn't enough.

## Installation

Easy methode:
1. Click the green "< > Code" button, then click "Download ZIP"

![1](https://github.com/user-attachments/assets/e255ebe3-834c-4c77-b408-f7a2ff33dc54)

2. Unzip the downloaded folder using something like 7zip.

![2](https://github.com/user-attachments/assets/116c5250-6237-49dc-94a6-ad07bc88346a)

3. Open the NoIPScan folder.
   
4. Double click the file called "NoIPScan.bat".
   
5. The python script will check for and ask permission to install any missing dependencies. Press y then enter to move forward.

Shell:
1. Open a terminal and clone repository.
```
git clone https://github.com/Nobody9714/NoIPScan.git
```
2. Move into the directory.
```
cd NoIPScan
```
3. Run the python script.
```
python NoIPScan.py
```
4. The python script will check for and ask permission to install any missing dependencies. Press y then enter to move forward.


## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `scapy`
  - `netifaces`
  - `mac_vendor_lookup`

You can install the required libraries using pip:

```
pip install scapy netifaces mac-vendor-lookup
```


## Disclaimer

This tool is intended for use on networks you own or have permission to scan. Always ensure you have the necessary authorization before scanning any network.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Donation

Monaro (XMR):  
46ReDpJp11aG3rDfR5dprQQdYfaCuZxXHgqpGhV6zWJUaG8RAuL8zcH2aSht73z6oFYzpNAuwUJVeAe4fD61Q7vAKmjdZjr

![xmrqr512](https://github.com/user-attachments/assets/43cba4d9-e3cd-4e57-9dde-7e8b976f7de9)


Polygon (MATIC):  
0x185Cf68c8A69c6b22De3D531B339B5D362067304

![maticqr512](https://github.com/user-attachments/assets/b1f27ef3-ddb8-42de-b2a6-bbe9309442e0)


Solana (SOL):  
Ccz6zf12AJB1xweDZ3SHhfJB9VgLxL52iLKjtzHL2nSb

---

Thank you for using NoIPScan!
