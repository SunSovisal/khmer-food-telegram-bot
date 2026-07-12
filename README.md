# ម្ហូបអ្វីថ្ងៃនេះ? — Khmer Food Telegram Bot

A Khmer-first Telegram bot that helps choose what to cook from the vegetables
and protein available at home. It includes more than 50 common Khmer household
dish variants across fish, chicken, pork, beef, shrimp, duck, egg, and meat-free
choices.

All text and buttons your mom sees inside Telegram are in Khmer. English is
used only in this developer setup guide.

## What your mom does

1. Sends `/start` to the bot.
2. Selects one or more vegetables and taps **រួចហើយ** (done).
3. Selects fish, chicken, pork, beef, shrimp, duck, egg, or no meat.
4. Gets five matching dish ideas in Khmer.
5. Taps a dish for a short description, asks for more ideas, or starts again.

## Deploy to Vercel (recommended)

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot`, follow its instructions, and copy the bot token.
3. Generate a webhook secret in a terminal:

   ```bash
   openssl rand -hex 32
   ```

4. Import this folder into Vercel (through a Git repository or the Vercel CLI).
5. In the Vercel project's **Settings → Environment Variables**, add:

   - `BOT_TOKEN`: the token from BotFather
   - `WEBHOOK_SECRET`: the random value generated in step 3

6. Deploy the project. Vercel will expose the function at:

   ```text
   https://YOUR-PROJECT.vercel.app/api/webhook
   ```

7. Register that HTTPS endpoint with Telegram. Set the three values first,
   then run the command:

   ```bash
   export BOT_TOKEN='paste-the-token-from-BotFather-here'
   export WEBHOOK_SECRET='paste-the-same-Vercel-secret-here'
   export WEBHOOK_URL='https://YOUR-PROJECT.vercel.app/api/webhook'

   curl -sS "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
     -H 'Content-Type: application/json' \
     --data "{\"url\":\"${WEBHOOK_URL}\",\"secret_token\":\"${WEBHOOK_SECRET}\",\"allowed_updates\":[\"message\",\"callback_query\"]}"
   ```

   Telegram should return `{"ok":true,...}`.

8. Open the bot in Telegram and send `/start`.

The bot is stateless: ingredient choices are stored compactly in its Telegram
buttons, so it does not need a database and works across separate Vercel
Function invocations. `WEBHOOK_SECRET` is checked on every incoming request.

Never post or commit either secret. The project has no third-party Python
dependencies.

## Run locally instead

Telegram cannot use a webhook and `getUpdates` polling simultaneously. Remove
the webhook, export the token, and run Python 3.10 or newer:

```bash
export BOT_TOKEN='paste-the-token-from-BotFather-here'
curl -sS "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook"
python3 bot.py
```

Local polling requires the terminal to stay open. Register the Vercel webhook
again when switching back to hosted mode.

## Optional BotFather menu commands

Send `/setcommands` to BotFather, choose the bot, and paste:

```text
start - ចាប់ផ្ដើមជ្រើសមុខម្ហូប
menu - ជ្រើសមុខម្ហូបម្ដងទៀត
help - របៀបប្រើ
```

## Customize the food list

- Edit `VEGETABLES` or `MEATS` in `dishes.py` to change the buttons.
- Add another `Dish(...)` item to `DISHES` to teach it a family recipe.
- The `proteins` and `vegetables` values must use keys from those two lists.

Recipes naturally vary by Cambodian family and province. The descriptions are
short suggestions, not claims that one version is the only authentic recipe.

## Test

```bash
python3 -m unittest discover -s tests -v
```
