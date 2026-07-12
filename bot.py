"""Khmer daily dish suggestion Telegram bot using only Python's stdlib."""

from __future__ import annotations

import html
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from dishes import DISHES, MEATS, VEGETABLES, Dish
from recommender import matching_vegetables, recommend_dishes


@dataclass
class Session:
    vegetables: set[str] = field(default_factory=set)
    meat: str | None = None
    result_offset: int = 0


VEGETABLE_KEYS = tuple(VEGETABLES)
VEGETABLE_MASK_LIMIT = (1 << len(VEGETABLE_KEYS)) - 1


def encode_vegetables(selected: set[str]) -> str:
    """Encode selected vegetables as a compact hexadecimal bitmask."""
    mask = 0
    for index, key in enumerate(VEGETABLE_KEYS):
        if key in selected:
            mask |= 1 << index
    return format(mask, "x")


def decode_vegetables(encoded: str) -> set[str]:
    """Decode and validate a vegetable bitmask received from Telegram."""
    if not encoded or len(encoded) > 8:
        raise ValueError("Invalid vegetable state")
    mask = int(encoded, 16)
    if mask < 0 or mask > VEGETABLE_MASK_LIMIT:
        raise ValueError("Vegetable state is outside the valid range")
    return {
        key for index, key in enumerate(VEGETABLE_KEYS)
        if mask & (1 << index)
    }


class TelegramError(RuntimeError):
    pass


class TelegramAPI:
    def __init__(self, token: str) -> None:
        self.base_url = f"https://api.telegram.org/bot{token}/"

    def call(self, method: str, **payload: Any) -> Any:
        request = urllib.request.Request(
            self.base_url + method,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise TelegramError(f"Telegram request failed: {type(error).__name__}") from error
        if not body.get("ok"):
            raise TelegramError(body.get("description", "Unknown Telegram API error"))
        return body.get("result")


class KhmerFoodBot:
    def __init__(self, api: TelegramAPI) -> None:
        self.api = api
        self.dishes_by_id = {dish.id: dish for dish in DISHES}

    @staticmethod
    def vegetable_keyboard(selected: set[str]) -> dict[str, Any]:
        buttons = []
        items = list(VEGETABLES.items())
        for index in range(0, len(items), 2):
            row = []
            for key, label in items[index : index + 2]:
                mark = "✅ " if key in selected else "▫️ "
                toggled = selected ^ {key}
                row.append({
                    "text": mark + label,
                    "callback_data": f"v:{encode_vegetables(toggled)}",
                })
            buttons.append(row)
        state = encode_vegetables(selected)
        buttons.append([{"text": "រួចហើយ ➡️", "callback_data": f"vd:{state}"}])
        return {"inline_keyboard": buttons}

    @staticmethod
    def meat_keyboard(selected: set[str]) -> dict[str, Any]:
        icons = {
            "fish": "🐟", "chicken": "🐓", "pork": "🐖", "beef": "🐄",
            "shrimp": "🦐", "duck": "🦆", "egg": "🥚", "none": "🥬",
        }
        items = list(MEATS.items())
        state = encode_vegetables(selected)
        rows = []
        for index in range(0, len(items), 2):
            rows.append([
                {"text": f"{icons[key]} {label}", "callback_data": f"m:{key}:{state}"}
                for key, label in items[index : index + 2]
            ])
        rows.append([{"text": "⬅️ ជ្រើសបន្លែវិញ", "callback_data": f"bv:{state}"}])
        return {"inline_keyboard": rows}

    def start_text(self, session: Session) -> str:
        if session.vegetables:
            selected = "، ".join(VEGETABLES[key] for key in VEGETABLES if key in session.vegetables)
            summary = f"\n\nបានជ្រើស៖ <b>{html.escape(selected)}</b>"
        else:
            summary = ""
        return (
            "👩‍🍳 <b>ថ្ងៃនេះធ្វើម្ហូបអ្វី?</b>\n\n"
            "សូមជ្រើសរើសបន្លែដែលមាននៅផ្ទះ។ អាចជ្រើសបានច្រើនមុខ "
            "ហើយចុច «រួចហើយ»។"
            + summary
        )

    def begin(self, chat_id: int, *, message_id: int | None = None) -> None:
        session = Session()
        payload = {
            "chat_id": chat_id,
            "text": self.start_text(session),
            "parse_mode": "HTML",
            "reply_markup": self.vegetable_keyboard(session.vegetables),
        }
        if message_id is None:
            self.api.call("sendMessage", **payload)
        else:
            payload["message_id"] = message_id
            self.api.call("editMessageText", **payload)

    def show_meat_choice(self, chat_id: int, message_id: int, session: Session) -> None:
        selected = "، ".join(VEGETABLES[key] for key in VEGETABLES if key in session.vegetables)
        selected = selected or "មិនបានជ្រើសបន្លែ"
        self.api.call(
            "editMessageText",
            chat_id=chat_id,
            message_id=message_id,
            text=(
                f"🥬 បន្លែ៖ <b>{html.escape(selected)}</b>\n\n"
                "ឥឡូវសូមជ្រើសរើសសាច់ ឬគ្រឿងប្រូតេអ៊ីនមួយមុខ៖"
            ),
            parse_mode="HTML",
            reply_markup=self.meat_keyboard(session.vegetables),
        )

    def results_keyboard(self, session: Session, dishes: list[Dish]) -> dict[str, Any]:
        state = encode_vegetables(session.vegetables)
        meat = session.meat or "none"
        context = f"{meat}:{state}:{session.result_offset}"
        rows = [
            [{"text": f"ℹ️ {dish.name_km}", "callback_data": f"d:{dish.id}:{context}"}]
            for dish in dishes
        ]
        rows.append([
            {
                "text": "🔄 មុខម្ហូបផ្សេងទៀត",
                "callback_data": f"r:{meat}:{state}:{session.result_offset + 5}",
            },
            {"text": "🥬 ជ្រើសម្ដងទៀត", "callback_data": "restart"},
        ])
        return {"inline_keyboard": rows}

    def result_text(self, session: Session, dishes: list[Dish]) -> str:
        veg_labels = [VEGETABLES[key] for key in VEGETABLES if key in session.vegetables]
        chosen_veg = "، ".join(veg_labels) or "មិនបានជ្រើសបន្លែ"
        lines = [
            "🍲 <b>មុខម្ហូបដែលអាចធ្វើថ្ងៃនេះ</b>",
            f"🥬 បន្លែ៖ {html.escape(chosen_veg)}",
            f"🍗 សាច់៖ {html.escape(MEATS[session.meat or 'none'])}",
            "",
        ]
        for index, dish in enumerate(dishes, 1):
            matches = matching_vegetables(dish, session.vegetables)
            match_text = "، ".join(VEGETABLES[key] for key in VEGETABLES if key in matches)
            why = f" — ប្រើ {html.escape(match_text)}" if match_text else ""
            lines.append(f"{index}. <b>{html.escape(dish.name_km)}</b>{why}")
            lines.append(f"   <i>{html.escape(dish.note_km)}</i>")
        lines.append("\nចុចលើឈ្មោះម្ហូប ដើម្បីមើលព័ត៌មានបន្ថែម។")
        return "\n".join(lines)

    def show_results(self, chat_id: int, message_id: int, session: Session) -> None:
        dishes = recommend_dishes(
            session.vegetables,
            session.meat or "none",
            limit=5,
            offset=session.result_offset,
        )
        self.api.call(
            "editMessageText",
            chat_id=chat_id,
            message_id=message_id,
            text=self.result_text(session, dishes),
            parse_mode="HTML",
            reply_markup=self.results_keyboard(session, dishes),
        )

    def show_dish(self, chat_id: int, message_id: int, session: Session, dish: Dish) -> None:
        dish_veg = [VEGETABLES[key] for key in dish.vegetables if key in VEGETABLES]
        ingredients = "، ".join(dish_veg) or "គ្រឿងផ្សំតាមរូបមន្តគ្រួសារ"
        state = encode_vegetables(session.vegetables)
        back_data = f"r:{session.meat or 'none'}:{state}:{session.result_offset}"
        self.api.call(
            "editMessageText",
            chat_id=chat_id,
            message_id=message_id,
            text=(
                f"🍽 <b>{html.escape(dish.name_km)}</b>\n"
                "\n"
                f"ប្រភេទ៖ {html.escape(dish.category_km)}\n"
                f"បន្លែដែលគេនិយមប្រើ៖ {html.escape(ingredients)}\n\n"
                f"{html.escape(dish.note_km)}\n\n"
                "ចំណាំ៖ រូបមន្តតាមផ្ទះនីមួយៗអាចប្រើគ្រឿងខុសគ្នាបន្តិច។"
            ),
            parse_mode="HTML",
            reply_markup={"inline_keyboard": [[
                {"text": "⬅️ ត្រឡប់ទៅបញ្ជី", "callback_data": back_data},
                {"text": "🥬 ជ្រើសម្ដងទៀត", "callback_data": "restart"},
            ]]},
        )

    def handle_callback(self, callback: dict[str, Any]) -> None:
        callback_id = callback["id"]
        message = callback.get("message")
        if not message:
            self.api.call("answerCallbackQuery", callback_query_id=callback_id)
            return
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        data = callback.get("data", "")

        self.api.call("answerCallbackQuery", callback_query_id=callback_id)

        if data == "restart":
            self.begin(chat_id, message_id=message_id)
            return

        try:
            if data.startswith("v:"):
                session = Session(vegetables=decode_vegetables(data.split(":", 1)[1]))
                self.api.call(
                    "editMessageText",
                    chat_id=chat_id,
                    message_id=message_id,
                    text=self.start_text(session),
                    parse_mode="HTML",
                    reply_markup=self.vegetable_keyboard(session.vegetables),
                )
            elif data.startswith("vd:"):
                session = Session(vegetables=decode_vegetables(data.split(":", 1)[1]))
                self.show_meat_choice(chat_id, message_id, session)
            elif data.startswith("bv:"):
                session = Session(vegetables=decode_vegetables(data.split(":", 1)[1]))
                self.api.call(
                    "editMessageText",
                    chat_id=chat_id,
                    message_id=message_id,
                    text=self.start_text(session),
                    parse_mode="HTML",
                    reply_markup=self.vegetable_keyboard(session.vegetables),
                )
            elif data.startswith("m:"):
                _, meat, encoded = data.split(":")
                if meat not in MEATS:
                    raise ValueError("Unknown protein")
                session = Session(vegetables=decode_vegetables(encoded), meat=meat)
                self.show_results(chat_id, message_id, session)
            elif data.startswith("r:"):
                _, meat, encoded, raw_offset = data.split(":")
                if meat not in MEATS:
                    raise ValueError("Unknown protein")
                offset = int(raw_offset)
                if offset < 0 or offset > 10_000:
                    raise ValueError("Invalid result offset")
                session = Session(
                    vegetables=decode_vegetables(encoded),
                    meat=meat,
                    result_offset=offset,
                )
                self.show_results(chat_id, message_id, session)
            elif data.startswith("d:"):
                _, dish_id, meat, encoded, raw_offset = data.split(":")
                if meat not in MEATS:
                    raise ValueError("Unknown protein")
                offset = int(raw_offset)
                if offset < 0 or offset > 10_000:
                    raise ValueError("Invalid result offset")
                session = Session(
                    vegetables=decode_vegetables(encoded),
                    meat=meat,
                    result_offset=offset,
                )
                dish = self.dishes_by_id.get(dish_id)
                visible_ids = {
                    item.id for item in recommend_dishes(
                        session.vegetables, meat, limit=5, offset=offset
                    )
                }
                if dish is None or dish.id not in visible_ids:
                    raise ValueError("Dish is not in this result page")
                self.show_dish(chat_id, message_id, session, dish)
            else:
                raise ValueError("Unknown callback")
        except (TypeError, ValueError):
            # Old or tampered buttons safely restart instead of depending on
            # any process-local memory.
            self.begin(chat_id, message_id=message_id)

    def handle_update(self, update: dict[str, Any]) -> None:
        if "callback_query" in update:
            self.handle_callback(update["callback_query"])
            return
        message = update.get("message")
        if not message or "text" not in message:
            return
        chat_id = message["chat"]["id"]
        text = message["text"].strip().split()[0].split("@")[0].lower()
        if text in {"/start", "/menu", "/help"}:
            self.begin(chat_id)
        else:
            self.api.call(
                "sendMessage",
                chat_id=chat_id,
                text="សូមចុច /start ដើម្បីជ្រើសបន្លែ និងរកមុខម្ហូបសម្រាប់ថ្ងៃនេះ។",
            )


def main() -> int:
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        print("BOT_TOKEN is missing. See README.md for setup instructions.", file=sys.stderr)
        return 2

    api = TelegramAPI(token)
    bot = KhmerFoodBot(api)
    try:
        profile = api.call("getMe")
        print(f"Running @{profile['username']} — press Ctrl+C to stop", flush=True)
        offset = 0
        while True:
            try:
                updates = api.call(
                    "getUpdates",
                    offset=offset,
                    timeout=25,
                    allowed_updates=["message", "callback_query"],
                )
                for update in updates:
                    offset = update["update_id"] + 1
                    try:
                        bot.handle_update(update)
                    except TelegramError as error:
                        print(f"Could not handle update {update['update_id']}: {error}", file=sys.stderr)
            except TelegramError as error:
                print(f"Polling error: {error}; retrying in 3 seconds", file=sys.stderr)
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nBot stopped.")
        return 0
    except TelegramError as error:
        print(f"Could not start bot: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
