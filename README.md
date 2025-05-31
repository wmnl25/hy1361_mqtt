# HY1361 Sound Level Meter MQTT Script

A simple script to read out the HY1361 sound level meter and publish the data to an MQTT server.

---

## Usage

Add the following MQTT sensor configuration to your Home Assistant setup:

```yaml
mqtt:
  - sensor:
      - name: "Sound Level Meter"
        state_topic: "soundmeter/spl"
        unit_of_measurement: "dB"
        value_template: "{{ value | float }}"
