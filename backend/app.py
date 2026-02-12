from flask import Flask, jsonify, render_template
import threading
import time
from engine import monitor
from engine import alerts
from database import conn

app = Flask(__name__, static_folder='static', 
                      template_folder='templates')

def start_monitoring():
    while True:
        try:
            monitor()
        except Exception as e:
            print(f"Monitor loop error: {e}")
            time.sleep(5)




@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/alerts")
def get_alerts():
    try:
        return jsonify(alerts[-10:])  
    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@app.route("/history")
def get_history():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY time DESC LIMIT 10")
    history = cursor.fetchall()
    return jsonify(history)

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitor_thread.start() 
    app.run(debug=True, host='0.0.0.0', port=5000)
    
   
