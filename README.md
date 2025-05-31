Just a simple script to readout the HY1361 sound level meter and publish it to a MQTT server.

Use

mqtt:
  - sensor:
      - name: "Sound Level Meter"
        state_topic: "soundmeter/spl"
        unit_of_measurement: "dB"
        value_template: "{{ value | float }}"

To add to Home Assistant
