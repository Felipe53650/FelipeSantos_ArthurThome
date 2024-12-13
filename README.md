## Apache Kafka com Docker Compose

Alunos:

- Felipe Santos
- Arthur Thomé

### Descrição

Este projeto configura e cria um ambiente Apache Kafka utilizando Docker Compose.

O ambiente é composto por:

- 3 nodos
- Um Zookeeper
- Interface Gráfica KAFKA UI

### Pré-requisitos

Em sua máquina, certifique-se de ter instalado os softwares abaixo:

- Visual Studio Code (com extensão Python)
- Docker Desktop
- Docker Compose

(talvez durante o uso do terminal CMD, será necessário instalar algumas bibliotecas como kafka e six).

## Instalação

1. Baixe o arquivo docker-compose.yml, em anexo neste repositório.

2. Inicie a Docker Engine (certifique-se ed que ela está habilitada nessas opções de configurações)

![image](https://github.com/user-attachments/assets/9e2741a7-35b9-4b0e-977d-8ee319870413)

![image](https://github.com/user-attachments/assets/5d958f2a-fe1c-45d9-adc5-188cef1b7d4e)

3. No terminal, navegue até o diretório onde está salvo o arquivo YAML, e após, inicie os containers

```
 docker-compose up -d
´´´

```
4. Verifique se os containers estão funcionando corretamente

```
docker ps
´´´
```
É esperado que apareça os containers:

- kafka-ui
- zookeeper
- kafkas 1, 2 e 3

### Etapas do trabalho

## 1. A criação do ambiente cluster

   - 3 nodos kafka (com fator de replicação 3 partições, conectados ao Zookeeper)
   - Interface gráfica Kafka UI (vai simplificar o monitoramento e a criação de tópicos e mensagens)

   Essa configuração de tópico foi feita no Kafka UI.

## 2. Produtor e Consumidor (Todos os nodos ligados)

1. Acesse o Kafka UI pelo endereço URL http://localhost:8080

2. Crie um tópico na interface, exemplo (teste-topico) com 3 partições e fator de replicação 3.

3. Produza mensagens no tópico, indo no menu Tópico e acessando a aba Produce Message

## 3. Produtor e consumidor (com UM nodo desligado)

1. Pare um dos brokers kafka, como por exemplo, kafka3:

```
docker stop 'nome_do_container'
´´´
```
Pode repetir todas as operaçoes de produtor e consumidor na interface gráfica, e o cluster continuará funcionando por conta do fator de replicação configurado no ambiente/tópico.
   
3. Agora, reinicie o nodo kafka que foi desligado

```
docker start 'nome do container' 
´´´
  
```
(Caso não saiba o nome do container, pode revisar-lo pelo comando:

```
docker ps
´´´´
```
## 4. Produtor e Consumidor (com um nodo a mais)

1. Edite o arquivo docker-compose.yml para acrescentar um novo broker kafka

```
kafka4:
  image: confluentinc/cp-kafka:latest
  depends_on:
    - zookeeper
  ports:
    - "9095:9095"
  environment:
    KAFKA_BROKER_ID: 4
    KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka4:9095
    KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9095
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
    KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3
    KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2
´´´
```
2. Inclua kafka4:9095 na varíavel KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS. Isso irá atualizar o bootstrap do cluster

```
KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS: kafka1:9092,kafka2:9093,kafka3:9094,kafka4:9095
´´´
```
3. Suba o novo serviço
```
docker-compose up -d
´´´
```
4. Reinicie todos os serviços para garantir que o novo nodo seja reconhecido pela interface gráfica.

```
docker-compose restart kafka1 kafka2 kafka3 kafka4 (os kafkas/containers você deve escrever conforme o nome dado a eles)
´´´
````
5. Agora, verifique o status na interface.

## Observação: para criar um consumidor em grupo, abra o VS Code e crie um script com o nome group_consumer.py

cole o código abaixo:

```
from kafka import KafkaConsumer
import json

# Configuração do consumidor
consumer = KafkaConsumer(
    'test-topic',  # Nome do tópico
    bootstrap_servers=['localhost:19092', 'localhost:29092', 'localhost:39092', 'localhost:9095'],  # Brokers
    group_id='test-group',  # Nome do grupo
    auto_offset_reset='earliest',  # Início da leitura (do começo)
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Decodificador para JSON
)

print("Consumidor iniciado. Aguardando mensagens...\n")

# Consumir mensagens
for message in consumer:
    print(f"Mensagem recebida: {message.value} na partição {message.partition}")
´´´
```
salve e execute-o em diferentes terminais para simular consumidores em grupo:
```
python group_consumer.py
´´´



