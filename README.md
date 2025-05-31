# HY1361 Sound Level Meter MQTT Script

A simple script to read out the HY1361 sound level meter and publish the data to an MQTT server.

---

## Usage

### Requirements

- Python 3
- `pyserial` package
- `paho-mqtt` package
- MQTT broker accessible with credentials

Install dependencies:

```bash
pip3 install pyserial paho-mqtt
```

### Add the following MQTT sensor configuration to your Home Assistant setup:

```yaml
mqtt:
  - sensor:
      - name: "Sound Level Meter"
        state_topic: "soundmeter/spl"
        unit_of_measurement: "dB"
        value_template: "{{ value | float }}"
```

### Running manually
Run the script directly for testing or manual operation:
```bash
python3 hy1361_mqtt.py
```

## Running as a systemd service
Create the service unit file

1. Create a new systemd service file:
```bash
sudo nano /etc/systemd/system/hy1361_mqtt.service
```
2.Paste the following service configuration
```bash
[Unit]
Description=HY1361 Sound Level Meter MQTT Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/hy1361_mqtt
ExecStart=/usr/bin/python3 /home/pi/hy1361_mqtt/hy1361_mqtt_service.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=hy1361_mqtt

[Install]
WantedBy=multi-user.target
```
Update paths and username (pi) as needed.

3. Reload systemd manager configuration
```bash
sudo systemctl daemon-reload
```
4. Enable the service to start on boot
```bash
sudo systemctl enable hy1361_mqtt.service
```
5. Start the service immediately
```bash
sudo systemctl start hy1361_mqtt.service
```
6. Check the status of the service
```bash
sudo systemctl status hy1361_mqtt.service
```


## Configuration
MQTT broker IP, port, username, and password are configured inside hy1361_mqtt_service.py (edit variables at the top).

The serial port defaults to /dev/ttyUSB0, but can be changed in the script if your device is on a different port.

The MQTT topic used is soundmeter/spl.

## Troubleshooting
Ensure the user running the service (pi in example) has read/write access to the serial device /dev/ttyUSB0.

Check service logs via journalctl -u hy1361_mqtt for detailed error messages.

The service automatically attempts reconnects on MQTT or serial connection failures.

If you change the service file, always run sudo systemctl daemon-reload before restarting the service.

