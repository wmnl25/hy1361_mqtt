import serial
import time
import struct
import paho.mqtt.client as mqtt
import logging
import sys

MQTT_BROKER = "my_ip"
MQTT_PORT = 1883
MQTT_USER = "my_user"
MQTT_PASS = "my_password"
MQTT_TOPIC = "soundmeter/spl"
SERIAL_PORT = '/dev/ttyUSB0'

# Setup logging (outputs to stdout, systemd captures this)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)

class HY1361:
    def __init__(self, port=SERIAL_PORT):
        self.port = port
        self.ser = None
        self.connect_serial()

    def connect_serial(self):
        while True:
            try:
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=115200,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=1
                )
                logging.info(f"Connected to HY1361 on {self.port}")
                break
            except serial.SerialException as e:
                logging.error(f"Serial connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def read_packet(self):
        while True:
            try:
                byte = self.ser.read(1)
                if byte == b'\x55':  # Start byte
                    frame = byte + self.ser.read(5)
                    if len(frame) == 6 and frame[5] == 0xAA:
                        value = struct.unpack('<H', frame[2:4])[0]
                        return value / 10.0
                    else:
                        logging.warning(f"Invalid packet: {frame.hex()}")
                else:
                    continue
            except serial.SerialException as e:
                logging.error(f"Serial read error: {e}. Attempting to reconnect...")
                self.connect_serial()
            except Exception as e:
                logging.error(f"Unexpected error reading serial data: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully")
    else:
        logging.error(f"Failed to connect to MQTT Broker, return code {rc}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logging.error(f"MQTT connection failed: {e}")
        sys.exit(1)

    client.loop_start()

    meter = HY1361()

    try:
        while True:
            spl = meter.read_packet()
            logging.info(f"Sound Level: {spl:.1f} dB")
            client.publish(MQTT_TOPIC, f"{spl:.1f}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("Exiting on user interrupt")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
