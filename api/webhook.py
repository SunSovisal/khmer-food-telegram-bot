"""Vercel Function receiving Telegram webhook updates."""

from __future__ import annotations

import hmac
import json
import os
from http.server import BaseHTTPRequestHandler
from typing import Any

from bot import KhmerFoodBot, TelegramAPI, TelegramError


MAX_REQUEST_BYTES = 1_000_000


class handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, body: dict[str, Any]) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        self.send_json(200, {"ok": True, "service": "khmer-food-telegram-bot"})

    def do_POST(self) -> None:
        token = os.environ.get("BOT_TOKEN", "").strip()
        secret = os.environ.get("WEBHOOK_SECRET", "").strip()
        if not token or not secret:
            self.send_json(500, {"ok": False, "error": "Server is not configured"})
            return

        supplied_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not hmac.compare_digest(supplied_secret, secret):
            self.send_json(403, {"ok": False, "error": "Forbidden"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
                raise ValueError("Invalid request size")
            update = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(update, dict) or "update_id" not in update:
                raise ValueError("Invalid Telegram update")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self.send_json(400, {"ok": False, "error": "Invalid request"})
            return

        try:
            KhmerFoodBot(TelegramAPI(token)).handle_update(update)
        except TelegramError:
            # A non-2xx response asks Telegram to retry delivery later.
            self.send_json(502, {"ok": False, "error": "Telegram API request failed"})
            return

        self.send_json(200, {"ok": True})


    def log_message(self, format: str, *args: Any) -> None:
        # Vercel already records request logs; avoid duplicating them.
        return

