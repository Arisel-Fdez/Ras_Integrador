import smbus2 
# instancia I2C
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

# Register direcciones dl MAX30100
REG_INTR_STATUS = 0x00 
REG_INTR_ENABLE = 0x01
REG_FIFO_WR_PTR = 0x02
REG_OVF_COUNTER = 0x03
REG_FIFO_RD_PTR = 0x04
REG_FIFO_DATA = 0x05
REG_MODE_CONFIG = 0x06
REG_SPO2_CONFIG = 0x07
REG_LED_CONFIG = 0x09

class MAX30100:
    def __init__(self, address=0x57, bus_num=1): # I2C
        self.address = address
        self.bus = smbus2.SMBus(bus_num)
        self.reset()
        time.sleep(1)  
        self.setup()

# CM
    def shutdown(self): # A
        self.bus.write_byte_data(self.address, REG_MODE_CONFIG, 0x80)

    def reset(self):
        self.bus.write_byte_data(self.address, REG_MODE_CONFIG, 0x40)

    def setup(self):                                                             # Cg
        self.bus.write_byte_data(self.address, REG_INTR_ENABLE, 0xc0)
        self.bus.write_byte_data(self.address, REG_FIFO_WR_PTR, 0x00)
        self.bus.write_byte_data(self.address, REG_OVF_COUNTER, 0x00)
        self.bus.write_byte_data(self.address, REG_FIFO_RD_PTR, 0x00)
        self.bus.write_byte_data(self.address, REG_MODE_CONFIG, 0x03)  
        self.bus.write_byte_data(self.address, REG_SPO2_CONFIG, 0x27)
        self.bus.write_byte_data(self.address, REG_LED_CONFIG, 0x24)
        print("Sensor setup complete")

    def set_leds(self, red_level, ir_level):
        self.bus.write_byte_data(self.address, 0x0C, red_level)  
        self.bus.write_byte_data(self.address, 0x0D, ir_level) 

    def read_sensor(self):                                            # Lr
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x05, 4)
            self.ir = (data[0] << 8) | data[1]
            self.red = (data[2] << 8) | data[3]
            return self.ir, self.red
        except OSError as e:
            print(f"Error reading MAX30100 sensor: {e}")
            self.bus.close()
            time.sleep(1)
            self.bus = smbus2.SMBus(1)
            return None, None

def read_max30100():
    sensor = MAX30100()
    
    # Set initial LED brightness levels (values range from 0 to 255)
    sensor.set_leds(0x24, 0x24)  
    
    try:
        while True:
            ir, red = sensor.read_sensor()
            if ir is not None and red is not None:
                hr = ir / 100.0  # Simulación de lectura de ritmo cardíaco
                spo2 = red / 100.0  # Simulación de lectura de SPO2
                message = f"MAX30100 - HR: {hr:.2f}, SpO2: {spo2:.2f}"
                print(message)
                client.publish(MQTT_TOPIC, message)
            else:
                print("Error reading MAX30100 sensor data")
            time.sleep(0.750)  # Reduce el tiempo de espera para obtener lecturas más frecuentes
    except KeyboardInterrupt:
        print("Sensor shutdown")
        sensor.shutdown()
        client.disconnect()
