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
