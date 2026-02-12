import time
import numpy as np
import mindspore as ms
import os
from mindspore import Tensor, nn
from model import AutoEncoder
from data import generate_sample
from database import save_alert


ms.context.set_context(mode=ms.context.PYNATIVE_MODE)
ms.set_device("CPU")



model = AutoEncoder(input_dim=39)
ckpt_path = "autoencoder_nslkdd.ckpt"
if os.path.exists(ckpt_path):
    print(f"Loading checkpoint from {ckpt_path}")   
    ms.load_checkpoint("autoencoder_nslkdd.ckpt", net=model)
else:
    print(f"Checkpoint not found at {ckpt_path}. Using untrained model.")
    
loss_fn = nn.MSELoss()
THRESHOLD = 5.0
alerts = []

def monitor():
    global alerts
    
    
    while True:
        try: 
             status = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "severity": "normal",
                "score": 0.0
            }

             anomaly = np.random.rand() > 0.8
             x = generate_sample(anomaly)
             x_t = Tensor(x, ms.float32)
             recon = model(x_t)
             loss = loss_fn(recon, x_t).asnumpy()


             if loss > THRESHOLD:
                alert_data = {
                     "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                     "severity": "HIGH",
                     "score": float(loss)
                }
                alerts.append(alert_data)
                save_alert(alert_data)
                if len(alerts) > 1000:
                    alerts.pop(0)
                print(f"ALERT:{alert_data}")
             else:
                 alerts.append(status)    

             time.sleep(2)

        except Exception as e: 
            print(f"Monitor loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor()   
