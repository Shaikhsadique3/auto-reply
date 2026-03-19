import time
import random
from playwright.sync_api import sync_playwright
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

EMAIL = os.getenv("X_EMAIL")
PASSWORD = os.getenv("X_PASSWORD")

KEYWORDS = [
    "saas onboarding",
    "user activation",
    "trial conversion",
]

def generate_reply(tweet):
    prompt = f"""
You are a SaaS founder replying on X.

Rules:
- 1-2 lines
- human tone
- no marketing
- helpful

Tweet:
{tweet}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # login
        page.goto("https://x.com/login")
        page.fill('input[name="text"]', EMAIL)
        page.keyboard.press("Enter")
        time.sleep(2)

        page.fill('input[name="password"]', PASSWORD)
        page.keyboard.press("Enter")
        time.sleep(5)

        replies_done = 0

        while replies_done < 20:  # start small
            keyword = random.choice(KEYWORDS)

            page.goto(f"https://x.com/search?q={keyword}&src=typed_query&f=live")
            time.sleep(5)

            tweets = page.locator("article").all()

            for tweet in tweets[:3]:
                try:
                    text = tweet.inner_text()

                    reply = generate_reply(text)

                    tweet.click()
                    time.sleep(3)

                    page.locator('div[role="textbox"]').fill(reply)
                    page.keyboard.press("Control+Enter")

                    print("Replied:", reply)

                    replies_done += 1

                    time.sleep(random.randint(600, 1500))  # 10–25 min

                except Exception as e:
                    print("Error:", e)
                    continue

        browser.close()


if __name__ == "__main__":
    run_bot()
