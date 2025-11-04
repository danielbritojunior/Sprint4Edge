# ⚽ Projeto "Passa a Bola" - Sprint 4: Edge Computing

## 1. Introdução

Este repositório contém o projeto final da Sprint 4 para a disciplina de "Edge Computing and Computer Systems".

O objetivo deste projeto é demonstrar uma **Prova de Conceito (PoC)** de uma arquitetura IoT funcional. Para isso, foi construído um **Placar de Futebol Inteligente** que opera em tempo real.

Este sistema simula a deteção de gols para dois times usando sensores. Os dados são enviados (publicados) via MQTT para um broker na nuvem, e um dashboard web (site) recebe (subscreve) esses dados, atualizando um placar visual para o utilizador instantaneamente.

Este repositório contém todos os "códigos-fonte finais" e "scripts de deploy" necessários para replicar o projeto.

---

## 👥 Integrantes

* Daniel Brito dos Santos Junior - RM 566236
* Gustavo Palomares Borsato - RM 564621
* Vitor Rampazzi Franco - RM 562270

---

## 🛠️ Arquitetura e Componentes

A solução é dividida em três partes que comunicam entre si:

### 1. O Hardware (Dispositivo IoT)

O dispositivo que deteta os gols foi simulado na plataforma Wokwi para garantir a replicabilidade. Ele é composto por:

* **1x Placa ESP32:** O "cérebro" do projeto, responsável por ler os sensores, controlar o LCD e (o mais importante) conectar-se ao Wi-Fi para enviar os dados.
* **2x Sensores Ultrassónicos HC-SR04:** Usados para simular a passagem da bola pela linha do gol. Cada sensor representa o gol de um time. Quando a distância lida é curta (< 10cm), ele regista um "gol".
* **1x Display LCD 16x2 I2C:** Mostra o placar localmente no hardware ("Time A: 0 | Time B: 0").
* **1x Buzzer:** Emite um som temático ("Olé, Olé") a cada gol marcado, com tons diferentes para cada time.

### 2. O Broker (Plataforma de Gerenciamento)

Atua como o "carteiro" ou intermediário na nuvem. O hardware e o site nunca se falam diretamente; eles falam através do broker.

* **Plataforma:** Broker MQTT (FIWARE/IoT da disciplina)
* **Endereço:** `54.221.163.3`
* **Porta:** `1883`

### 3. O Dashboard (Servidor e Site)

Este é o site que o utilizador vê. É um servidor local escrito em Python que:
1.  Liga-se ao Broker MQTT para "ouvir" os gols.
2.  Usa **Flask** para criar uma página web.
3.  Usa **Flask-SocketIO** para "empurrar" o novo placar para o navegador em tempo real (sem precisar de recarregar a página).

---

## 🗂️ Estrutura do Repositório

Para garantir a "organização por pastas", os arquivos estão divididos da seguinte forma:

```
/Sprint4Edge/
├── /hardware-dispositivo/
│   └── placar_esp32.ino     # (Código-fonte do ESP32 que vai no Wokwi)
│
├── /servidor-dashboard/
│   ├── dashboard_python.py       # (Código do nosso site/servidor Python)
│   └── requirements.txt     # (O "script de deploy" com as bibliotecas Python)
│
└── README.md                # (Esta documentação)
```

---

## 🚀 Como Executar o Projeto

Esta secção é a "garantia de replicabilidade". Siga estes passos para testar o projeto completo no seu computador.

### Pré-requisitos

Antes de começar, garanta que tem duas ferramentas instaladas no seu computador:
1.  **Git** (para copiar o repositório).
2.  **Python** (versão 3.7 ou superior).

### Passo 1: Clonar (Copiar) o Repositório

Abra o seu Terminal (ou `cmd`) e use o `git clone` para copiar os ficheiros para o seu computador.

```bash
git clone [https://github.com/danielbritojunior/Sprint4Edge.git](https://github.com/danielbritojunior/Sprint4Edge.git)
```
Depois, entre na pasta que acabou de ser criada:
```bash
cd Sprint4Edge
```

### Passo 2: Iniciar o Hardware

Você tem duas opções para iniciar o hardware. Para a entrega online, use a Opção A. Para uma apresentação presencial, use a Opção B.

#### Opção A: Simulado (Wokwi - Recomendado para Teste Rápido)

1.  Abra o seu navegador de Internet.
2.  Aceda ao nosso link público de simulação no Wokwi:
    * **Link:** https://wokwi.com/projects/446647076897545217
3.  Clique no botão verde "►" (Play) para iniciar a simulação.
4.  No Wokwi, na aba "Serial Monitor" (embaixo), aguarde até ver as mensagens:
    * `WiFi Conectado!`
    * `Conectado ao Broker MQTT... Conectado!`

O seu hardware está agora online e pronto para enviar gols.

#### Opção B: Método Local (Presencial com Placa Real)

Isto é para quando você for montar o projeto fisicamente.

1.  **Monte o Circuito:** Conecte os componentes físicos (LCD, 2x Sensores, Buzzer) nos pinos do ESP32 conforme definido no código (`placar_esp32.ino`).
2.  **Abra o Código:** Abra o ficheiro `/hardware-dispositivo/placar_esp32.ino` na sua Arduino IDE.
3.  **Instale as Bibliotecas:** No Arduino IDE, vá a `Ferramentas > Gerir Bibliotecas...` e instale:
    * `PubSubClient`
    * `ArduinoJson`
    * `LiquidCrystal_I2C`
4.  **Altere o Wi-Fi:** Mude as linhas 10 e 11 do código para o Wi-Fi do local (ex: o hotspot do seu telemóvel):
    ```cpp
    const char* SSID = "Nome_do_WiFi_do_seu_Telemovel";
    const char* PASSWORD = "Senha_do_seu_WiFi";
    ```
5.  **Carregue o Código:** Clique em "Carregar" (Upload) no Arduino IDE para enviar o código para a sua placa ESP32.

### Passo 3: Iniciar o Servidor do Dashboard (o seu PC)

(Este passo é o mesmo, quer o hardware seja real ou simulado)

1.  **Volte ao seu Terminal** (que já está dentro da pasta `Sprint4Edge`).
2.  Navegue para a pasta do servidor:
    ```bash
    cd servidor-dashboard
    ```
3.  **Instale as bibliotecas:** Use o nosso "script de deploy" (`requirements.txt`) para instalar tudo o que o Python precisa:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o servidor:**
    ```bash
    python dashboard_python.py
    ```

Se tudo correu bem, o seu terminal vai mostrar:
`[MQTT] Conectado ao Broker '54.221.163.3'...`
`Iniciando servidor Flask... a rodar em http://0.0.0.0:5000/`

### Passo 4: Ver o Placar!

1.  Abra o seu navegador (Chrome, Firefox, etc.).
2.  Aceda ao endereço: `http://127.0.0.1:5000` (ou `http://localhost:5000`).
3.  O seu placar deve aparecer.

Agora, **coloque o Wokwi (ou o seu hardware real) e o seu navegador lado a lado** para ver a magia acontecer.

---

## 📸 Resultados da PoC (Prints da Integração)

Estes são os "prints de integração IoT com o site" que comprovam o funcionamento:

### 1. Sistema Conectado (Visão Geral)
O Wokwi (esquerda) está conectado ao Broker. O Servidor Python (terminal) também está conectado. O Dashboard (navegador) mostra o placar inicial "0 vs 0".

<img width="1364" height="624" alt="image" src="https://github.com/user-attachments/assets/d3e5cbc8-c08f-4944-92b2-951f88c475ca" />

### 2. PoC: Gol do Time A (Publicação HW -> Site)
Simulamos um gol no sensor do Time A (clicando no sensor esquerdo no Wokwi). O placar no site (direita) atualizou **instantaneamente** para "1" com a animação "pop".

<img width="1913" height="903" alt="image" src="https://github.com/user-attachments/assets/1b00693d-4cf6-4ccf-b66e-b6fa5ca0ebad" />


### 3. PoC: Fim de Jogo (Comando Site -> HW)
Clicamos em "Encerrar e Resetar" no site. O Modal de "Fim de Jogo" (com o vencedor) apareceu no navegador.

<img width="1915" height="900" alt="image" src="https://github.com/user-attachments/assets/0add8bfc-cb88-47e2-a9ef-1ff71d90f7e5" />


### 4. PoC: Confirmação no Hardware
Após clicar em "Ok, Fechar", o comando foi enviado ao ESP32 (Wokwi), que mostrou o vencedor no seu próprio LCD antes de zerar os contadores.

<img width="926" height="450" alt="image" src="https://github.com/user-attachments/assets/72cca058-59ef-46e2-a386-52a5aea5888f" />
