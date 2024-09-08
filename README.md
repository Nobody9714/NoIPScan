Summary:
"NoIPScan.py" is a simple yet powerful tool that scans your local network for connected devices, providing a list of discovered devices. All without grayware, ads, data harvesting, or deceptive download links.

Features:
Network Scanning: Scan your local network  for device's hostname, NIC Vendor, IP address and MAC address. Includes optional multiple scans attemps because sometimes 1 just isnt enough.
Device Identification: Uses various methodes to identify the device. Including a MAC address lookup using https://api.macvendors.com over https (read more below) to identify the NIC vendor. 
Disable MAC Lookup: Disables the MAC address lookup encase your worried about it.
Sort Options: Click the column headers to sort the devices alphanumaricly.
Copy: Right click to copy an entry for a specific device.
Web Browser Integration: Right click or highlight a device and select "Open in Browser" to open the selected device's IP address in your default web browser. Some devices may require a port or more specific path.

Install Instructions:

Easy methode:
1. Click the green "< > Code" Button, then click "Download Zip".
2. Go to your downloads folder and extract the file using something like 7zip, then open the folder called "NoIPScan".
3. Launch the file called "Start NoIPScan".
4. Follow the prompts as you may need to install the below requirments to run the script.
5. Done! You should be able to use the network scanner now.

Shell methode:
1. Clone this repository using git clone https://github.com/Nobody9714/NoIPScan.git. 
2. Navigate into the project directory with cd NoIPScan. 
3. Run the script using Python: python NoIPScan.py.
4. Install the requirments when prompted to.
5. Done! You should be able to use the network scanner now.

Requirements:
Python: Version 3.x or higher. 
tkinter: A built-in Python library; ensure it's enabled in your Python installation. 
asyncio: Used for asynchronous programming, included with Python 3.5 and later versions.
webbrowser: For opening web browsers directly from the application (default package). 
queue: Used to handle concurrent requests and responses; part of the standard library in Python 3.x. 
threading: Enables multithreading for improved performance, included with Python's standard library.

Uninstall:
The IP scanner its self isnt ever "Installed". The IP scanner is just a python script thats ran using a batch file to make it more user friendly. The only things that get installed are the requirments to run the script. You can uninstall the requirments you dont want by opening powershell and using the relative command(s): 



Donations:
If you find this script useful or would like to show your thanks, consider donating using 1 of the following wallet addresses:

Please only donate the native token (e.g. SOL, MATIC, XMR) or the token of the DePIN project you found this github from.

Monaro (XMR):  
46ReDpJp11aG3rDfR5dprQQdYfaCuZxXHgqpGhV6zWJUaG8RAuL8zcH2aSht73z6oFYzpNAuwUJVeAe4fD61Q7vAKmjdZjr

![xmrqr512](https://github.com/user-attachments/assets/43cba4d9-e3cd-4e57-9dde-7e8b976f7de9)


Polygon (MATIC):  
0x185Cf68c8A69c6b22De3D531B339B5D362067304

![maticqr512](https://github.com/user-attachments/assets/b1f27ef3-ddb8-42de-b2a6-bbe9309442e0)


Solana (SOL):  
Ccz6zf12AJB1xweDZ3SHhfJB9VgLxL52iLKjtzHL2nSb

![solqr512](https://github.com/user-attachments/assets/425d31fa-8cb0-4a1f-aaac-df3d22083d83)


