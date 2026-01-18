"""
Classe base para workers que processam mensagens de filas RabbitMQ.
"""

from abc import ABC, abstractmethod

from utils.broker import get_rabbitmq_connection
from utils.logging import get_logger


class BaseWorker(ABC):
    """
    Classe base para workers. Encapsula a configuração do RabbitMQ e o loop de consumo.
    """

    def __init__(self, queue_name: str, agent_class=None):
        """
        Inicializa o worker.

        Args:
            queue_name (str): Nome da fila a ser consumida.
            agent_class: Classe do agente a ser instanciada (opcional).
        """
        self.queue_name = queue_name
        self.agent = agent_class() if agent_class else None
        self.logger = get_logger(self.__class__.__name__)
        self.connection = None
        self.channel = None

    def setup_connection(self):
        """Configura a conexão e canal do RabbitMQ."""
        self.connection = get_rabbitmq_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    @abstractmethod
    def process_message(self, ch, method, properties, body):
        """
        Método abstrato para processar mensagens da fila.

        Args:
            ch: Canal do RabbitMQ.
            method: Método de entrega.
            properties: Propriedades da mensagem.
            body: Corpo da mensagem (bytes).
        """
        pass

    def run(self):
        """Inicia o consumo de mensagens da fila."""
        self.setup_connection()
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.process_message
        )
        self.logger.info(f"{self.__class__.__name__} esperando mensagens...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Interrupção detectada, fechando conexão...")
            self.channel.stop_consuming()
            self.connection.close()
