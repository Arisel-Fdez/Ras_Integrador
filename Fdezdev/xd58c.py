import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Configuración de MQTT
MQTT_SERVER = "44.198.205.23"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32.mqtt"
MQTT_USER = "guest"
MQTT_PASSWORD = "guest"

# Configurar el cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Configuración del sensor Xd58c Ritmo
XD58C_PIN = 17  # GPIO 17 conectado al pin 11 de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(XD58C_PIN, GPIO.IN)

def read_xd58c():
    try:
        while True:
            ritmo = GPIO.input(XD58C_PIN)
            message= f"Xd58c Ritmo - Pulso: {ritmo}"
            print(message)
            client.publish(MQTT_TOPIC, message)
            time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
