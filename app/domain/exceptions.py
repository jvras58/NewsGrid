class MessageBrokerError(Exception):
    """Erro genérico relacionado ao broker de mensagens."""

    def __init__(self, message: str, queue_name: str = None, data_summary: str = None):
        super().__init__(message)
        self.queue_name = queue_name
        self.data_summary = data_summary

    def __str__(self):
        details = f"Fila: {self.queue_name}" if self.queue_name else ""
        if self.data_summary:
            details += f" | Dados: {self.data_summary}"
        return f"{super().__str__()} | {details}"


class RabbitMQConnectionError(MessageBrokerError):
    """Erro específico de conexão com RabbitMQ."""

    pass


class MessageSendError(MessageBrokerError):
    """Erro ao enviar mensagem para a fila."""

    pass
