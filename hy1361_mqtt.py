import serial
import time
import struct
import paho.mqtt.client as mqtt

MQTT_BROKER = "10.7.7.130"
MQTT_PORT = 1883
MQTT_USER = "my_user"
MQTT_PASS = "my_password"
MQTT_TOPIC = "soundmeter/spl"

class HY1361:
    def __init__(self, port='/dev/ttyUSB0'):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            print(f"Connected to HY1361 on {port}")
        except serial.SerialException as e:
            print("Serial connection error:", e)
            exit(1)

    def read_packet(self):
        while True:
            byte = self.ser.read(1)
            if byte == b'\x55':  # Start byte
                frame = byte + self.ser.read(5)
                if len(frame) == 6 and frame[5] == 0xAA:
                    value = struct.unpack('<H', frame[2:4])[0]
                    return value / 10.0
                else:
                    print(f"Invalid packet: {frame.hex()}")
            else:
                continue

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")

if __name__ == "__main__":
    # Setup MQTT client
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    meter = HY1361()

    try:
        while True:
            spl = meter.read_packet()
            print(f"Sound Level: {spl:.1f} dB")
            client.publish(MQTT_TOPIC, f"{spl:.1f}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        client.disconnect()
