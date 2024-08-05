import threading
from mlx90614 import read_mlx90614
from max30100 import read_max30100
from xd58c import read_xd58c
                

# Crear hilos para cada sensor
thread_mlx = threading.Thread(target=read_mlx90614)
thread_max = threading.Thread(target=read_max30100)
thread_xd58c = threading.Thread(target=read_xd58c)

# Iniciar los hilos
thread_mlx.start()
thread_max.start()
thread_xd58c.start()
    
# Unir los hilos para que el programa principal espere su finalización 
thread_mlx.join()
thread_max.join()
thread_xd58c.join()
          