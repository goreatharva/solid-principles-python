
"""I — Interface Segregation Principle (ISP)

Clients should not be forced to depend on methods they do not use.
We split communication capabilities into small interfaces and build
clients that depend only on what they need.
"""
from __future__ import annotations
from abc import ABC, abstractmethod

class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None: ...

class SMSSender(ABC):
    @abstractmethod
    def send_sms(self, to: str, body: str) -> None: ...

class BasicEmailService(EmailSender):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str, str]] = []

    def send_email(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, subject, body))

class BasicSMSService(SMSSender):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send_sms(self, to: str, body: str) -> None:
        self.sent.append((to, body))

class EmailNotifier:
    def __init__(self, mailer: EmailSender) -> None:
        self.mailer = mailer

    def notify(self, to: str, subject: str, body: str) -> None:
        self.mailer.send_email(to, subject, body)

class SMSNotifier:
    def __init__(self, sms: SMSSender) -> None:
        self.sms = sms

    def notify(self, to: str, body: str) -> None:
        self.sms.send_sms(to, body)
