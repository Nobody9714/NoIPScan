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
   
3. Agree to install any missing dependencies.
   
5. Everything in the program should be fine to leave as default. Just press the "Scan Network" button to scan for devices on your local network.

   Optional:
   
   a. Custom network address.
   
   b. Custom IP range from 1-254
   
   c. Hide MAC Address, toggle to hide/unhide all mac addresses.
   
   d. Disable MAC Address lookup on https://api.macvendors.com. This is encase you dont want to use this to help identify devices more thoroughly than just IP and MAC addresses.

   e. # of scans to do on the network because sometimes 1 isn't enough.

## Installation

Easy methode:
1. Click the green "< > Code" button, then click "Download ZIP"
   
3. Unzip the downloaded folder using something like 7zip.
   
5. Open the NoIPScan folder.
   
7. Double click the "NoIPScann.bat" file.
   
9. The python script will check for and ask permission to install any missing dependencies. Press y then enter to move forward.

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

## Donation

If you find NoIPScan useful and would like to support its development, consider making a donation to the creator. [Add your preferred donation method and link here]

## License

[Include your chosen license information here]

## Disclaimer

This tool is intended for use on networks you own or have permission to scan. Always ensure you have the necessary authorization before scanning any network.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

---

Thank you for using NoIPScan!
