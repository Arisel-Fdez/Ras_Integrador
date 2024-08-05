import board
import busio
from adafruit_mlx90614 import MLX90614
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

# Configuración del sensor MLX90614
i2c = busio.I2C(board.SCL, board.SDA)
mlx_sensor = MLX90614(i2c)

def read_mlx90614():
    try:
        while True:
            ambient_temp = mlx_sensor.ambient_temperature
            object_temp = mlx_sensor.object_temperature
            message = f"MLX90614 - Ambient: {ambient_temp:.2f} C, Object: {object_temp:.2f} C"
            print(message)
            client.publish(MQTT_TOPIC, message)
            time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()