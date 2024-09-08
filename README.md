## Summary

NoIPScan is a Python script designed to scan your local network for connected devices. I made this python script so there is an IP scanner option that is not full of bloatware, spyware, ads, data harvesting, or deceiving download links like you'll find on most websites. This tool was developed with the assistance of Claude 3.5 Sonnet and other generative AI models for everything including code, readme forematting, and images. Then edited as necessary.

## Features

- Fast and efficient IP scanning
- Automatic detection of local IP range
- Concurrent scanning for improved speed
- Various means to help identify devices other than using IP/MAC addresses.
- Alphanumerically sortable list by either clicking the headers or right clicking in the list > sort > sorting option.
- Disable MAC address lookup using https://api.macvendors.com. This will keep the scan local and not send requests out to macvendors in search for more device information. Slightly increasing scan speed but also making it harder to identify what the devices on your network are.
  
## How to Use

1. Double click the file called "NoIpScan.bat".
   
2. Agree to install any missing dependencies.
   
3. Everything in the program should be fine to leave as default. Just press the "Scan Network" button to scan for devices on your local network.

   ![program](https://github.com/user-attachments/assets/eaadccf0-22a5-4730-959a-a7b35c690312)

   Optional:
   
   a. Custom network address.
   
   b. Custom IP range from 1-254
   
   c. Hide MAC Address, toggle to hide/unhide all mac addresses.
   
   d. Disable MAC Address lookup on https://api.macvendors.com. This is encase you dont want to use online 3rd parties to help you identify devices on your network.

   e. # of scans to do on the network because sometimes 1 isn't enough.

   f. Right click an entry in the list for more options.

## Requirements

- [Python 3.6 or higher]([/wiki/contributing-guidelines](https://www.python.org/downloads/windows/)) (may need to manually install.)
- Required Python libraries (will be installed automaticlly):
  - `tkinter (usually included with Python)`
  - `PIL (Python Imaging Library)`
  - `netifaces`
  - `getmac`
  - `aiohttp`


## Installation

Easy methode:
1. Click the green "< > Code" button, then click "Download ZIP"

![1](https://github.com/user-attachments/assets/e255ebe3-834c-4c77-b408-f7a2ff33dc54)

2. Unzip the downloaded folder using something like 7zip.

![2](https://github.com/user-attachments/assets/116c5250-6237-49dc-94a6-ad07bc88346a)

3. Open the folder "NoIPScan-main".
   
4. Double click the file called "NoIPScan.bat".
   
5. The python script will check for and ask permission to install any missing dependencies. Press y then enter to move forward.

Shell methode:
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


## Uninstall

Theres nothing to uninstall because its just a python script. If you want to uninstall the python libraries, you can do so in powershell with:

```
pip uninstall (libraryname)
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

![solqr512](https://github.com/user-attachments/assets/e54fe04d-326f-4660-96fc-c6ca23f84006)

---

Thank you for using NoIPScan!
