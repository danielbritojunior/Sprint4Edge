```markdown
# ⚽ Projeto "Passa a Bola" - Sprint 4: Edge Computing

Este repositório contém a Prova de Conceito (PoC) da Sprint 4 para a disciplina de "Edge Computing and Computer Systems", conforme os requisitos da Entrega 2.

O objetivo foi implementar uma arquitetura IoT funcional, demonstrando a comunicação em tempo real (publicação e subscrição) entre um dispositivo IoT (hardware simulado) e uma plataforma de visualização (dashboard web).

---

## 👥 Integrantes

* [NOME COMPLETO DO INTEGRANTE 1 - RM XXXXX]
* [NOME COMPLETO DO INTEGRANTE 2 - RM XXXXX]
* [NOME COMPLETO DO INTEGRANTE 3 - RM XXXXX]
* [NOME COMPLETO DO INTEGRANTE 4 - RM XXXXX]

---

## 📋 Detalhes da Implementação

A arquitetura da solução é baseada em 3 componentes principais que comunicam via protocolo MQTT:

1.  **Dispositivo IoT (Hardware Simulado):**
    * **Plataforma:** Wokwi (Simulador de ESP32).
    * **Hardware:** 1x ESP32, 2x Sensores Ultrassónicos HC-SR04 (um para cada time), 1x Display LCD 16x2 I2C e 1x Buzzer.
    * **Função:** Deteta a passagem da "bola" (simulada pela alteração da distância no sensor), contabiliza os golos para o "Time A" ou "Time B", exibe o placar no LCD e toca uma melodia de "Olé, Olé" no buzzer.

2.  **Broker MQTT (Plataforma de Gerenciamento):**
    * **Endereço:** `54.221.163.3` (Broker FIWARE/IoT da disciplina).
    * **Porta:** `1883`.
    * **Função:** Atua como o intermediário que recebe as mensagens publicadas pelo ESP32 e as retransmite para todos os clientes subscritos (como o nosso dashboard).

3.  **Dashboard (Servidor e Frontend):**
    * **Tecnologia (Backend):** Um servidor web local escrito em Python, usando **Flask** (para servir a página) e **Flask-SocketIO** (para comunicação em tempo real com o navegador).
    * **Tecnologia (Frontend):** A interface é construída com HTML, CSS e JavaScript (jQuery), apresentando um placar "dark mode" que se atualiza instantaneamente.

### Comunicação Bidirecional

O projeto implementa comunicação nos dois sentidos:
* **HW -> Site (Publicação):** O ESP32 publica os golos nos tópicos `passa-a-bola/timeA/attrs` e `passa-a-bola/timeB/attrs`.
* **Site -> HW (Subscrição):** O Dashboard (site) publica uma mensagem `{"comando": "resetar"}` no tópico `passa-a-bola/baliza01/cmd`. O ESP32 está subscrito a este tópico, e ao receber o comando, exibe o vencedor no LCD e zera a contagem.

---

## 🗂️ Estrutura do Repositório (Organização por Pastas)

Os "códigos-fonte finais" estão "organizados por pastas" da seguinte forma:

```

/Sprint4Edge/
├── /hardware-dispositivo/
│   └── placar\_esp32.ino     \# (Código-fonte final do ESP32)
│
├── /servidor-dashboard/
│   ├── dashboard.py         \# (Código-fonte final do servidor Flask/SocketIO)
│   └── requirements.txt     \# (Script de deploy das bibliotecas Python)
│
└── README.md                \# (Esta documentação)

````

---

## 🚀 Como Replicar o Projeto (Garantia de Replicabilidade)

Para garantir a "garantia de replicabilidade do projeto" e testar a Prova de Conceito (PoC), siga os 3 passos abaixo.

### Passo 1: Iniciar o Hardware (Simulado)

1.  Aceda ao link do nosso projeto no Wokwi.
2.  Clique no botão verde "Play" (Iniciar Simulação).
3.  Aguarde o monitor série (em baixo) mostrar "WiFi Conectado!" e "Conectado ao Broker MQTT".

* **Link do Wokwi:** `[COLOQUE AQUI O SEU LINK PÚBLICO DO WOKWI]`
* (O código-fonte desta simulação também está disponível na pasta `/hardware-dispositivo/placar_esp32.ino`).

### Passo 2: Iniciar o Servidor do Dashboard (Local)

1.  Clone este repositório ou faça o download dos ficheiros.
2.  Abra um terminal e navegue até à pasta `/servidor-dashboard/`.
3.  Instale as bibliotecas Python usando o nosso "script de deploy" (`requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o servidor:
    ```bash
    python dashboard.py
    ```
5.  O seu terminal deve confirmar a ligação ao broker `54.221.163.3` e que o servidor está a rodar em `http://0.0.0.0:5000/`.

### Passo 3: Testar a Integração

1.  Abra o seu navegador (Chrome, Firefox, etc.) e aceda a `http://127.0.0.1:5000` (ou `http://localhost:5000`).
2.  O dashboard do placar deve aparecer e mostrar "Conectado" no topo.

---

## 📸 Resultados da PoC (Prints da Integração)

Abaixo estão os "prints de integração IoT com o site" que demonstram os "resultados da PoC" em funcionamento.

### 1. Sistema Conectado (Visão Geral)
O Wokwi (esquerda) está conectado ao Broker. O Servidor Python (terminal) também está conectado. O Dashboard (navegador) mostra o placar inicial "0 vs 0".

`[COLOQUE AQUI O SEU PRINT DO SISTEMA LIGADO]`

### 2. PoC: Golo do Time A (Publicação HW -> Site)
Simulámos um golo no sensor do Time A (esquerda). O placar no site (direita) atualizou **instantaneamente** para "1" com a animação "pop".

`[COLOQUE AQUI O SEU PRINT DO PLACAR A MOSTRAR "1 vs 0"]`

### 3. PoC: Fim de Jogo (Comando Site -> HW)
Clicámos em "Encerrar e Resetar" no site. O Modal de "Fim de Jogo" apareceu no navegador.

`[COLOQUE AQUI O SEU PRINT DO MODAL DE "FIM DE JOGO" NO SITE]`

### 4. PoC: Confirmação no Hardware
Após clicar em "Ok, Fechar" no Modal, o comando foi enviado ao ESP32, que mostrou o vencedor no LCD antes de zerar os contadores.

`[COLOQUE AQUI UM PRINT DO LCD NO WOKWI A MOSTRAR "Time A Venceu!"]`
````