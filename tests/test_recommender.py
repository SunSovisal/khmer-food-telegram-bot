import unittest

from bot import (
    KhmerFoodBot,
    Session,
    decode_vegetables,
    encode_vegetables,
)
from dishes import DISHES, MEATS, VEGETABLES
from recommender import matching_vegetables, recommend_dishes


class RecommenderTests(unittest.TestCase):
    def test_recommendations_use_selected_protein(self):
        results = recommend_dishes({"potato", "carrot"}, "chicken")
        self.assertTrue(results)
        self.assertTrue(all("chicken" in dish.proteins for dish in results))

    def test_best_matching_dish_is_first(self):
        results = recommend_dishes({"potato", "carrot"}, "chicken")
        self.assertIn(results[0].id, {"chicken_curry", "braised_chicken_potato"})
        self.assertEqual(matching_vegetables(results[0], {"potato", "carrot"}), {"potato", "carrot"})

    def test_meat_free_results_stay_meat_free(self):
        results = recommend_dishes({"mushroom", "cabbage"}, "none")
        self.assertTrue(results)
        self.assertTrue(all(dish.proteins == ("none",) for dish in results))

    def test_more_results_cycles_safely(self):
        first = recommend_dishes({"mushroom"}, "duck", offset=0)
        more = recommend_dishes({"mushroom"}, "duck", offset=5)
        self.assertTrue(first)
        self.assertTrue(more)

    def test_dish_data_references_known_ingredients(self):
        dish_ids = set()
        for dish in DISHES:
            self.assertNotIn(dish.id, dish_ids)
            dish_ids.add(dish.id)
            self.assertTrue(set(dish.proteins) <= set(MEATS))
            self.assertTrue(set(dish.vegetables) <= set(VEGETABLES))


class FakeAPI:
    def __init__(self):
        self.calls = []

    def call(self, method, **payload):
        self.calls.append((method, payload))
        return {}


class KhmerInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeAPI()
        self.bot = KhmerFoodBot(self.api)

    def test_start_screen_is_khmer(self):
        self.bot.begin(chat_id=1)
        method, payload = self.api.calls[-1]
        self.assertEqual(method, "sendMessage")
        self.assertIn("ថ្ងៃនេះធ្វើម្ហូបអ្វី", payload["text"])
        button_texts = [
            button["text"]
            for row in payload["reply_markup"]["inline_keyboard"]
            for button in row
        ]
        self.assertIn("រួចហើយ ➡️", button_texts)

    def test_dish_detail_does_not_show_english_subtitle(self):
        session = Session(vegetables={"mushroom"}, meat="fish")
        dish = next(dish for dish in DISHES if dish.id == "steamed_fish_mushroom")
        self.bot.show_dish(chat_id=1, message_id=2, session=session, dish=dish)
        _, payload = self.api.calls[-1]
        self.assertIn(dish.name_km, payload["text"])
        self.assertNotIn(dish.name_en, payload["text"])

    def test_vegetable_state_round_trip(self):
        selected = {"mushroom", "water_spinach", "pumpkin", "lettuce"}
        self.assertEqual(decode_vegetables(encode_vegetables(selected)), selected)

    def test_flow_survives_a_fresh_bot_instance(self):
        self.bot.begin(chat_id=1)
        _, start_payload = self.api.calls[-1]
        first_vegetable = start_payload["reply_markup"]["inline_keyboard"][0][0]

        fresh_api = FakeAPI()
        fresh_bot = KhmerFoodBot(fresh_api)
        fresh_bot.handle_callback({
            "id": "callback-1",
            "from": {"id": 2},
            "data": first_vegetable["callback_data"],
            "message": {"message_id": 3, "chat": {"id": 1}},
        })

        method, payload = fresh_api.calls[-1]
        self.assertEqual(method, "editMessageText")
        self.assertIn("បានជ្រើស", payload["text"])

    def test_all_generated_callback_data_fits_telegram_limit(self):
        session = Session(
            vegetables=set(VEGETABLES),
            meat="chicken",
            result_offset=10_000,
        )
        keyboards = [
            self.bot.vegetable_keyboard(session.vegetables),
            self.bot.meat_keyboard(session.vegetables),
            self.bot.results_keyboard(
                session,
                recommend_dishes(session.vegetables, "chicken", limit=5),
            ),
        ]
        for keyboard in keyboards:
            for row in keyboard["inline_keyboard"]:
                for button in row:
                    self.assertLessEqual(len(button["callback_data"].encode("utf-8")), 64)


if __name__ == "__main__":
    unittest.main()
