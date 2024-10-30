import asyncio
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from db.models.user import UserORM


@dataclass
class EmailService:
    smtp_server: str
    smtp_port: int
    email: str
    password: str

    async def send_email(self, user_from: UserORM, user_to: UserORM) -> None:
        asyncio.create_task(self._send_email(user_from, user_to))


    async def _send_email(self, user_from: UserORM, user_to: UserORM):
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = user_to.email
        message['Subject'] = 'Match'
        body = f"""Вы понравились {user_from.first_name}! Почта участника: {user_from.email}»."""
        message.attach(MIMEText(body, 'plain'))


        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.email,
            password=self.password,
            start_tls=True
        )

