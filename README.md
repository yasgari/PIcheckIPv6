# PIcheckIPv6
Query Cisco Prime Infra for device configs and check to see if IPv6 is enabled. If the script finds running configs (sanitized) that do not have IPv6 enabled, it will export the device name, IP, and sanitized config to an Excel doc called 'deviceInfo.xlsx' in the same folder as the script.


## To use the script:

#### Clone the repo OR click on the green button "Code" above, and download as a ZIP file, then unzip.
```
git clone https://github.com/yasgari/PIcheckIPv6
```


#### CD into new folder and install required Python modules
```
cd PIcheckIPv6
```
```
pip3 install -r requirements.txt
```

#### Run script. 


```
python3 ipv6check.py PRIME-IP PRIME-USER PRIME-PASSWORD
```
Example command:  

```
python3 ipv6check.py 10.10.10.10 user123 pass123
```
