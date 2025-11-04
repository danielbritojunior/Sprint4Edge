from flask import Flask, render_template_string
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json


# --- Configurações do MQTT 
MQTT_BROKER    = "54.221.163.3" # IP do professor
MQTT_PORT      = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_DADOS = "passa-a-bola/+/attrs" 
MQTT_TOPIC_CMD   = "passa-a-bola/baliza01/cmd"
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
ultimo_placar_A = 0
ultimo_placar_B = 0

# ================== Lógica MQTT ==================

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Conectado ao Broker '{MQTT_BROKER}' com resultado: {rc}")
    client.subscribe(MQTT_TOPIC_DADOS)
    print(f"[MQTT] Subscrito em: {MQTT_TOPIC_DADOS}")

def on_message(client, userdata, msg):
    global ultimo_placar_A, ultimo_placar_B
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"[MQTT] Mensagem recebida em {msg.topic}: {payload_str}")
        topic_parts = msg.topic.split('/')
        time_id = topic_parts[1]
        data = json.loads(payload_str)
        if "gols" in data:
            total_gols = int(data["gols"])
            if time_id == "timeA":
                ultimo_placar_A = total_gols
                socketio.emit("novo_placar_A", {"gols": ultimo_placar_A})
                print(f"[SocketIO] Emitindo 'novo_placar_A': {ultimo_placar_A}")
            elif time_id == "timeB":
                ultimo_placar_B = total_gols
                socketio.emit("novo_placar_B", {"gols": ultimo_placar_B})
                print(f"[SocketIO] Emitindo 'novo_placar_B': {ultimo_placar_B}")
    except Exception as e:
        print(f"[ERRO] Falha ao processar mensagem MQTT: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
client.loop_start()

# ================== Rotas HTTP (Flask) ==================

@app.route("/")
def index():

    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Placar - Passa a Bola</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    
    <style>
        :root {
            --color-time-a: #0099ff; --color-time-b: #f1c40f; --color-bg: #1a1a2e;
            --color-card: #2a2a4e; --color-text: #f0f0f0; --color-danger: #e74c3c;
            --color-danger-hover: #c0392b;
        }
        body {
            font-family: 'Poppins', sans-serif; background-color: var(--color-bg);
            color: var(--color-text); display: flex; flex-direction: column;
            justify-content: center; align-items: center; height: 100vh;
            margin: 0; overflow: hidden;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 0; }
        .header .status { font-size: 1rem; color: #4caf50; height: 20px; }
        .placar-grid { display: flex; justify-content: center; align-items: stretch; gap: 30px; }
        .time-container {
            background-color: var(--color-card); padding: 30px 60px;
            border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            text-align: center; width: 300px; transition: all 0.3s ease;
        }
        .time-container h2 {
            font-size: 2rem; font-weight: 700; margin-top: 0; margin-bottom: 15px;
            padding-bottom: 10px; border-bottom: 4px solid var(--color-time-a);
        }
        .time-container.time-b h2 { border-bottom-color: var(--color-time-b); }
        .placar {
            font-size: 10rem; font-weight: 900; line-height: 1;
            color: #ffffff; transition: all 0.2s ease-in-out;
        }
        .vs-separator {
            display: flex; align-items: center; font-size: 3rem;
            font-weight: 900; color: var(--color-danger);
            text-shadow: 0 0 10px rgba(231, 76, 60, 0.5);
        }
        #btn-reset {
            margin-top: 40px; padding: 15px 30px; font-size: 1.1rem;
            font-weight: 700; color: #fff;
            background: linear-gradient(45deg, var(--color-danger), var(--color-danger-hover));
            border: none; border-radius: 8px; cursor: pointer;
            text-transform: uppercase; transition: all 0.3s ease;
        }
        #btn-reset:hover {
            transform: scale(1.05); box-shadow: 0 5px 20px rgba(231, 76, 60, 0.4);
        }
        @keyframes scorePop {
            0% { transform: scale(1); text-shadow: none; }
            50% { transform: scale(1.3); color: #fff; text-shadow: 0 0 25px #ffffff, 0 0 40px var(--color-time-a); }
            100% { transform: scale(1); text-shadow: none; }
        }
        @keyframes scorePopB {
            0% { transform: scale(1); text-shadow: none; }
            50% { transform: scale(1.3); color: #fff; text-shadow: 0 0 25px #ffffff, 0 0 40px var(--color-time-b); }
            100% { transform: scale(1); text-shadow: none; }
        }
        .score-update-a { animation: scorePop 0.4s ease-in-out; }
        .score-update-b { animation: scorePopB 0.4s ease-in-out; }

        #modal-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7);
            /* O Modal começa escondido */
            display: none; 
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        #modal-winner {
            background: #ffffff;
            color: #333;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 25px rgba(0,0,0,0.5);
            z-index: 101;
        }
        #modal-winner h2 {
            font-size: 2rem;
            font-weight: 700;
            margin-top: 0;
            color: var(--color-bg);
        }
        #modal-winner-text {
            font-size: 1.5rem;
            margin: 20px 0;
        }
        #modal-close-btn {
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: 700;
            color: #fff;
            background-color: var(--color-time-a);
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
    </style>
</head>
<body>
    <div class="header">
        <h1>Placar Tempo Real</h1>
        <div id="status" class="status"></div>
    </div>
    <div class="placar-grid">
        <div class="time-container time-a">
            <h2>Time A</h2> <div id="placar-A" class="placar">0</div>
        </div>
        <div class="vs-separator">VS</div>
        <div class="time-container time-b">
            <h2>Time B</h2> <div id="placar-B" class="placar">0</div>
        </div>
    </div>
    <button id="btn-reset">Encerrar e Resetar</button>

    <div id="modal-overlay">
        <div id="modal-winner">
            <h2>Fim de Jogo!</h2>
            <p id="modal-winner-text">Time A Venceu: 5 a 3</p>
            <button id="modal-close-btn">Ok, Fechar</button>
        </div>
    </div>
    <script>
        $(function() {
            const socket = io({ transports: ['websocket', 'polling'] });
            const statusEl = $('#status');
            const modalOverlay = $('#modal-overlay');
            const winnerText = $('#modal-winner-text');
            const placarA_El = $('#placar-A');
            const placarB_El = $('#placar-B');

            socket.on('connect', () => { statusEl.text('Conectado'); });
            socket.on('disconnect', () => { statusEl.text('Desconectado'); statusEl.css('color', 'var(--color-danger)'); });

            socket.on('novo_placar_A', (data) => {
                if (data && data.gols !== undefined) {
                    placarA_El.text(data.gols);
                    placarA_El.addClass('score-update-a');
                    setTimeout(() => { placarA_El.removeClass('score-update-a'); }, 400); 
                }
            });
            
            socket.on('novo_placar_B', (data) => {
                if (data && data.gols !== undefined) {
                    placarB_El.text(data.gols);
                    placarB_El.addClass('score-update-b');
                    setTimeout(() => { placarB_El.removeClass('score-update-b'); }, 400);
                }
            });

            socket.on('placar_atual', (data) => {
                if (data) {
                    placarA_El.text(data.gols_A || 0);
                    placarB_El.text(data.gols_B || 0);
                }
            });

            // --- AÇÃO: RESETAR (LÓGICA ATUALIZADA) ---
            $('#btn-reset').click(() => {
                
                let scoreA = parseInt(placarA_El.text()) || 0;
                let scoreB = parseInt(placarB_El.text()) || 0;
                let message = "";

                if (scoreA > scoreB) {
                    message = `TIME A VENCEU: ${scoreA} a ${scoreB}`;
                } else if (scoreB > scoreA) {
                    message = `TIME B VENCEU: ${scoreB} a ${scoreA}`;
                } else {
                    message = `EMPATE: ${scoreA} a ${scoreA}`;
                }

                // 2. Coloca a mensagem no modal
                winnerText.text(message);
                
                // 3. Mostra o modal (em vez do alert)
                modalOverlay.css('display', 'flex');
            });

            // --- NOVO: AÇÃO PARA FECHAR O MODAL ---
            $('#modal-close-btn').click(() => {
                // 1. Esconde o modal
                modalOverlay.css('display', 'none');
                
                // 2. AGORA SIM, envia o comando de reset
                console.log("Enviando comando 'resetar' para o servidor...");
                socket.emit('resetar');
                
                // 3. Zera o placar na tela
                placarA_El.text(0); 
                placarB_El.text(0); 
            });
        });
    </script>
</body>
</html>
    """)

# ================== Eventos SocketIO ==================

@socketio.on('connect')
def handle_connect():
    print("[SocketIO] Novo cliente conectado.")
    socketio.emit("placar_atual", {
        "gols_A": ultimo_placar_A,
        "gols_B": ultimo_placar_B
    })

@socketio.on('resetar')
def handle_reset():
    global ultimo_placar_A, ultimo_placar_B
    print("[SocketIO] Comando 'resetar' recebido do cliente.")
    
    if ultimo_placar_A > ultimo_placar_B:
        print(f"[GAME] Fim de jogo: Time A venceu ({ultimo_placar_A} a {ultimo_placar_B})")
    elif ultimo_placar_B > ultimo_placar_A:
        print(f"[GAME] Fim de jogo: Time B venceu ({ultimo_placar_B} a {ultimo_placar_A})")
    else:
        print(f"[GAME] Fim de jogo: Empate ({ultimo_placar_A} a {ultimo_placar_A})")

    payload_reset = json.dumps({"comando": "resetar"})
    client.publish(MQTT_TOPIC_CMD, payload_reset)
    print(f"[MQTT] Comando de reset publicado em: {MQTT_TOPIC_CMD}")
    
    ultimo_placar_A = 0
    ultimo_placar_B = 0
    socketio.emit("placar_atual", {"gols_A": 0, "gols_B": 0})

# ================== Main ==================
if __name__ == "__main__":
    print("Iniciando servidor Flask com SocketIO (v5 - Modal Vencedor)...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)