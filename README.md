## PiMonitor
A CPU utilization monitoring service for the Raspberry Pi 3 Model B implemented using the ClearBlade SDK and ClearBlade Platform.

### Quickstart
#### Monitor
First, on the ClearBlade platform, create a new System. Then, create a Device within this system. Next, clone this repository onto the Raspberry Pi and create a config file in the `monitor` directory named `clearblade.ini`. Fill in the details here with the information from the system and device you just created. Feel free to choose any channel name you like.

```ini
[system]
key = <system key>
secret = <system secret>

[device]
name = <device name>
active_key = <device active key>

[messaging]
channel = <channel name>
```

#### Service
Create a new Service on the ClearBlade platform in the System you created earlier. Add the following settings to this Service:
- Security: add the Authenticated role and allow it to execute the Service
- Requires: add the `clearblade` requirement
- Triggers: add a new trigger with source as `Messaging`, action as `Publish`, and topic equal to the channel name you set in the above configuration file.

Next, paste `service/cpuCollectionService.js` into the code box on the Service page on the ClearBlade platform site. 

#### Collection
Create a new Collection named `rpiCPU` in the same System you've been working in. Add the following columns:
- name: cpu_0, type: float
- name: cpu_1, type: float
- name: cpu_2, type: float
- name: cpu_3, type: float
- name: time, type: timestamp

#### Monitor, part 2
Finally, install and run the monitor.

```bash
# create a virtual environment
python3 -m venv venv
. venv/bin/activate
# install dependencies
pip install -r requirements.txt
# run monitor
cd monitor
python monitor.py
```

You should see rows start to show up on the Collection page on the ClearBlade platform.

