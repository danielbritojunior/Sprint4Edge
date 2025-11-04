# ⚽ Projeto "Passa a Bola" - Sprint 4: Edge Computing

## 1. Introdução

Este repositório contém o projeto final da Sprint 4 para a disciplina de "Edge Computing and Computer Systems".

O objetivo deste projeto é demonstrar uma **Prova de Conceito (PoC)** de uma arquitetura IoT funcional. Para isso, foi construído um **Placar de Futebol Inteligente** que opera em tempo real.

Este sistema simula a deteção de golos para dois times usando sensores. Os dados são enviados (publicados) via MQTT para um broker na nuvem, e um dashboard web (site) recebe (subscreve) esses dados, atualizando um placar visual para o utilizador instantaneamente.

Este repositório contém todos os "códigos-fonte finais" e "scripts de deploy" necessários para replicar o projeto.

---

## 👥 Integrantes

* [NOME COMPLETO DO INTEGRANTE 1 - RM XXXXX]
* [NOME COMPLETO DO INTEGRANTE 2 - RM XXXXX]
* [NOME COMPLETO DO INTEGRANTE 3 - RM XXXXX]
* 

---

## 🛠️ Arquitetura e Componentes

A solução é dividida em três partes que comunicam entre si:

### A. O Hardware (Dispositivo IoT)

O dispositivo que deteta os golos foi simulado na plataforma Wokwi para garantir a replicabilidade. Ele é composto por:

* **1x Placa ESP32:** O "cérebro" do projeto, responsável por ler os sensores, controlar o LCD e (o mais importante) conectar-se ao Wi-Fi para enviar os dados.
* **2x Sensores Ultrassónicos HC-SR04:** Usados para simular a baliza. Cada sensor representa um time. Quando a distância lida é curta (< 10cm), ele regista um "golo".
* **1x Display LCD 16x2 I2C:** Mostra o placar localmente no hardware ("Time A: 0 | Time B: 0").
* **1x Buzzer:** Emite um som temático ("Olé, Olé") a cada golo marcado, com tons diferentes para cada time.

### B. O Broker (Plataforma de Gerenciamento)

Atua como o "carteiro" ou intermediário na nuvem. O hardware e o site nunca se falam diretamente; eles falam através do broker.

* **Plataforma:** Broker MQTT (FIWARE/IoT da disciplina)
* **Endereço:** `54.221.163.3`
* **Porta:** `1883`

### C. O Dashboard (Servidor e Site)

Este é o "sitezinho" que o utilizador vê. É um servidor local escrito em Python que:
1.  Liga-se ao Broker MQTT para "ouvir" os golos.
2.  Usa **Flask** para criar uma página web.
3.  Usa **Flask-SocketIO** para "empurrar" o novo placar para o navegador em tempo real (sem precisar de recarregar a página).

---

## 🗂️ Estrutura do Repositório

Para garantir a "organização por pastas", os ficheiros estão divididos da seguinte forma:

```
/Sprint4Edge/
├── /hardware-dispositivo/
│   └── placar_esp32.ino     # (Código-fonte do ESP32 que vai no Wokwi)
│
├── /servidor-dashboard/
│   ├── dashboard.py         # (Código do nosso site/servidor Python)
│   └── requirements.txt     # (O "script de deploy" com as bibliotecas Python)
│
└── README.md                # (Esta documentação)
```

---

## 🚀 Como Executar o Projeto (Guia 100% Leigo)

Esta secção é a "garantia de replicabilidade". Siga estes passos para testar o projeto completo no seu computador.

### Pré-requisitos

Antes de começar, garanta que tem duas ferramentas instaladas no seu computador:
1.  **Git** (para copiar o repositório).
2.  **Python** (versão 3.7 ou superior).

### Passo 1: Clonar (Copiar) o Repositório

Abra o seu Terminal (ou `cmd`) e use o `git clone` para copiar os ficheiros para o seu computador.

```bash
git clone [COLE AQUI A URL DO SEU REPOSITÓRIO GIT]
```
Depois, entre na pasta que acabou de ser criada:
```bash
cd Sprint4Edge
```

### Passo 2: Iniciar o Hardware (Wokwi)

1.  Abra o seu navegador de Internet.
2.  Aceda ao nosso link público de simulação no Wokwi:
    * **Link:** `[COLOQUE AQUI O SEU LINK PÚBLICO DO WOKWI]`
3.  Clique no botão verde "►" (Play) para iniciar a simulação.
4.  No Wokwi, na aba "Serial Monitor" (em baixo), aguarde até ver as mensagens:
    * `WiFi Conectado!`
    * `Conectado ao Broker MQTT... Conectado!`

O seu hardware está agora online e pronto para enviar golos.

*(O código-fonte `.ino` que está a rodar no Wokwi também está guardado na pasta `/hardware-dispositivo` deste repositório).*

### Passo 3: Iniciar o Servidor do Dashboard (o seu PC)

Agora, vamos ligar o "sitezinho" (o `dashboard.py`) para ele receber os dados do Wokwi.

1.  **Volte ao seu Terminal** (que já está dentro da pasta `Sprint4Edge`).
2.  Navegue para a pasta do servidor:
    ```bash
    cd servidor-dashboard
    ```
3.  **(Opcional, mas recomendado)** Crie um ambiente virtual para não "sujar" o seu Python:
    ```bash
    python -m venv venv
    ```
4.  **Ative o ambiente virtual:**
    * No Windows: `.\venv\Scripts\activate`
    * No Mac/Linux: `source venv/bin/activate`

5.  **Instale as bibliotecas:** Use o nosso "script de deploy" (`requirements.txt`) para instalar tudo o que o Python precisa:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Execute o servidor:**
    ```bash
    python dashboard.py
    ```

Se tudo correu bem, o seu terminal vai mostrar:
`[MQTT] Conectado ao Broker '54.221.163.3'...`
`Iniciando servidor Flask... a rodar em http://0.0.0.0:5000/`

### Passo 4: Ver o Placar!

1.  Abra o seu navegador (Chrome, Firefox, etc.).
2.  Aceda ao endereço: `http://127.0.0.1:5000` (ou `http://localhost:5000`).
3.  O seu placar "dark mode" deve aparecer.

Agora, **coloque o Wokwi e o seu navegador lado a lado** para ver a magia acontecer.

---

## 📸 Resultados da PoC (Prints da Integração)

Estes são os "prints de integração IoT com o site" que comprovam o funcionamento:

### 1. Sistema Conectado (Visão Geral)
O Wokwi (esquerda) está conectado ao Broker. O Servidor Python (terminal) também está conectado. O Dashboard (navegador) mostra o placar inicial "0 vs 0".

`<img width="1364" height="624" alt="image" src="https://github.com/user-attachments/assets/78fc7dc7-1e10-44c9-8636-6cd2a8346d56" />
`

### 2. PoC: Golo do Time A (Publicação HW -> Site)
Simulámos um golo no sensor do Time A (clicando no sensor esquerdo no Wokwi). O placar no site (direita) atualizou **instantaneamente** para "1" com a animação "pop".

`[COLE AQUI O SEU PRINT DO PLACAR A MOSTRAR "1 vs 0"]`

### 3. PoC: Fim de Jogo (Comando Site -> HW)
Clicámos em "Encerrar e Resetar" no site. O Modal de "Fim de Jogo" (com o vencedor) apareceu no navegador.

`[COLE AQUI O SEU PRINT DO MODAL DE "FIM DE JOGO" NO SITE]`

### 4. PoC: Confirmação no Hardware
Após clicar em "Ok, Fechar" no Modal, o comando foi enviado ao ESP32 (Wokwi), que mostrou o vencedor no seu próprio LCD antes de zerar os contadores.

`[COLE AQUI UM PRINT DO LCD NO WOKWI A MOSTRAR "Time A Venceu!"]`
