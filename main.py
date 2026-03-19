import time
import random
import re
from playwright.sync_api import sync_playwright
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Upgraded to Pro model for better understanding and smarter replies
model = genai.GenerativeModel('gemini-1.5-pro')

EMAIL = os.getenv("X_EMAIL")
PASSWORD = os.getenv("X_PASSWORD")

# 6. Tweet Source Upgrade - High Value Keywords
KEYWORDS = [
    # Pain Points (Good for FirstWin promotion)
    '"activation rate" saas',
    '"trial conversion drop"',
    '"users not converting"',
    '"onboarding is broken"',
    '"churn rate is killing me"',
    '"user retention saas"',
    '"trial to paid conversion"',
    # Launches & Milestones (Good for networking/followers)
    '"launching my saas"',
    '"just launched on product hunt"',
    '"hit 1k MRR"',
    '"building in public"',
    '"first paying customer"',
    # General SaaS
    '"indie hacker saas"'
]

# 1. Intent Detection
def check_intent(tweet):
    prompt = f"""
Classify this tweet:

1 = SaaS problem
2 = SaaS discussion
3 = noise

Tweet:
{tweet}

Only return number (1, 2, or 3).
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "1" in text: return 1
        elif "2" in text: return 2
        else: return 3
    except Exception as e:
        print("Intent check error:", e)
        return 3

# 2. Founder Detection (AI)
def is_founder(bio):
    if not bio or len(bio.strip()) == 0:
        return False
    prompt = f"""
Is this person a SaaS founder or builder?

Bio:
{bio}

Answer 'yes' or 'no'.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().lower()
        return "yes" in text
    except Exception as e:
        print("Founder check error:", e)
        return False

# 4. Reply Engine V2 & 5. Smart Product Promotion
def generate_reply(tweet, intent, founder):
    prompt = f"""
You are a SaaS founder.

Write a reply:
- specific to this tweet
- show understanding
- give 1 insight or question
- 1–2 lines
- no generic advice

Tweet:
{tweet}
"""
    # Smart Product Promotion Rule
    if intent == 1 and founder:
        prompt += """\n
If relevant, mention FirstWin naturally as something you built to solve this.
No selling.
Example:
We’ve seen this a lot.
Users drop before hitting their first result.
That’s exactly why we built FirstWin.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Reply generation error:", e)
        return ""

# Helper function to get User Bio using Playwright
def get_user_bio(context, username):
    if not username:
        return ""
    bio = ""
    page = context.new_page()
    try:
        page.goto(f"https://x.com/{username}", timeout=15000)
        time.sleep(3)
        bio_locator = page.locator('[data-testid="UserDescription"]')
        if bio_locator.count() > 0:
            bio = bio_locator.first.inner_text()
    except Exception as e:
        print(f"Bio extract error for {username}:", e)
    finally:
        page.close()
    return bio

def process_tweet(page, browser_context, tweet, replies_done):
    try:
        tweet.scroll_into_view_if_needed()
        time.sleep(random.uniform(1.0, 3.0)) # Human-like scroll delay
        text = tweet.inner_text()
        
        # Username extract karna (bio ke liye)
        match = re.search(r'@(\w+)', text)
        username = match.group(1) if match else None
        
        # Likes extract karna (scoring ke liye)
        likes = 0
        try:
            like_aria = tweet.locator('[data-testid="like"]').get_attribute('aria-label', timeout=1000)
            if like_aria:
                l_match = re.search(r'(\d+)\s+Like', like_aria)
                if l_match:
                    likes = int(l_match.group(1))
        except:
            pass 

        print(f"\nProcessing tweet from @{username}...")

        # 1. Intent Check
        intent = check_intent(text)
        print(f"Intent Score (1=Problem, 2=Discussion, 3=Noise): {intent}")
        
        # Skip noise early to save time/API calls
        if intent == 3:
            print("[-] Noise detected. Skipping.")
            return replies_done

        # 2. Founder Check
        bio = get_user_bio(browser_context, username)
        founder = is_founder(bio)
        print(f"Is Founder?: {founder}")

        # 3. Priority Scoring Engine
        score = 0
        if intent == 1:
            score += 50
        if founder:
            score += 30
        if likes > 5:
            score += 20

        print(f"Final Priority Score: {score}")

        # Rule: if score >= 70 then reply
        if score >= 70:
            reply = generate_reply(text, intent, founder)
            if not reply:
                return replies_done
            
            print(f"[*] Replying: {reply}")
            
            # Anti-bot: Random delay before clicking reply
            time.sleep(random.uniform(2.0, 5.0))
            tweet.click()
            time.sleep(random.uniform(2.0, 4.0))

            # Anti-bot: Type like a human
            textbox = page.locator('div[role="textbox"]')
            textbox.click()
            time.sleep(1)
            for char in reply:
                page.keyboard.press(char)
                time.sleep(random.uniform(0.01, 0.1)) # Variable typing speed
            
            time.sleep(random.uniform(1.0, 2.0))
            page.keyboard.press("Control+Enter")

            print("[+] Replied successfully!")
            replies_done += 1

            # VERY SAFE Anti-bot: Random sleep after replying (3-5 mins)
            sleep_time = random.randint(180, 300)
            print(f"Sleeping for {sleep_time // 60} minutes and {sleep_time % 60} seconds to avoid ban...\n")
            time.sleep(sleep_time)
        else:
            print("[-] Score < 70, skipping this tweet.")
            # Small random delay between processing tweets
            time.sleep(random.uniform(2.0, 6.0))

    except Exception as e:
        print("Error processing tweet:", e)
    
    return replies_done

def run_bot():
    try:
        with sync_playwright() as p:
            # Use persistent context to save cookies and session state
            user_data_dir = os.path.join(os.getcwd(), "x_session")
            
            # Check if running on cloud (Render/Linux) or Local
            is_cloud = os.environ.get("RENDER") == "true" or not os.name == 'nt'
            
            # Add arguments to make it run smoothly on cloud/headless
            browser_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]

            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=True, # MUST be True for Cloud
                viewport={"width": 1280, "height": 720},
                args=browser_args
            )
            page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

            # Check if already logged in by navigating to home
            print("Checking login status...")
            page.goto("https://x.com/home", timeout=60000)
            time.sleep(5)
            
            if "login" in page.url or "i/flow/login" in page.url:
                print("Not logged in. Navigating to login page...")
                page.goto("https://x.com/login")
                time.sleep(5)
                
                try:
                    page.fill('input[autocomplete="username"]', EMAIL)
                    page.keyboard.press("Enter")
                    time.sleep(3)
                except:
                    pass # In case selector changes

                # Wait for password field (User can manually solve captchas/username checks in this time)
                print("Waiting for password field... (Please complete any captcha or username checks manually if asked)")
                try:
                    page.wait_for_selector('input[name="password"]', timeout=60000)
                    page.fill('input[name="password"]', PASSWORD)
                    page.keyboard.press("Enter")
                    time.sleep(5)
                    print("Waiting for login to complete... (Complete any 2FA or final checks manually)")
                    # Wait for the URL to change away from login
                    page.wait_for_url("**/home", timeout=120000)
                    print("Logged in successfully! Session saved.")
                except Exception as e:
                    print("Login failed or timed out. If you see 'Could not log you in now', try logging in manually in the opened browser window.")
                    print("I will wait for 3 minutes for you to log in manually...")
                    try:
                        page.wait_for_url("**/home", timeout=180000)
                        print("Manual login successful! Session saved.")
                    except:
                        print("Manual login also timed out. Closing browser.")
                        browser_context.close()
                        return
            else:
                print("Already logged in! Using saved session.")

            replies_done = 0
            # Safety limit: Maximum 100 replies per day to avoid suspension
            MAX_DAILY_REPLIES = 100

            # 7. Daily Strategy - V2 limits with Feed Checking
            while replies_done < MAX_DAILY_REPLIES: 
                # Decide whether to check Home Feed (30% chance) or Search Keyword (70% chance)
                if random.random() < 0.30:
                    print("\n--- Checking Home Feed ('For You') ---")
                    page.goto("https://x.com/home", timeout=60000)
                    time.sleep(random.uniform(5.0, 8.0))
                    
                    # Scroll a bit to load feed like a human
                    for _ in range(3):
                        page.keyboard.press("PageDown")
                        time.sleep(random.uniform(1.0, 2.0))
                    
                    tweets = page.locator("article").all()
                    # Process top 3 tweets from feed
                    for tweet in tweets[:3]:
                        replies_done = process_tweet(page, browser_context, tweet, replies_done)
                        if replies_done >= MAX_DAILY_REPLIES: break
                else:
                    keyword = random.choice(KEYWORDS)
                    print(f"\n--- Searching for: {keyword} ---")

                    page.goto(f"https://x.com/search?q={keyword}&src=typed_query&f=live")
                    time.sleep(random.uniform(5.0, 8.0))

                    tweets = page.locator("article").all()

                    for tweet in tweets[:5]: # Top 5 tweets check karna
                        replies_done = process_tweet(page, browser_context, tweet, replies_done)
                        if replies_done >= MAX_DAILY_REPLIES: break
                
                # Extra safety delay between cycles
                cycle_delay = random.randint(30, 120)
                print(f"Cycle finished. Waiting {cycle_delay} seconds before next action...")
                time.sleep(cycle_delay)

            print("Daily limit reached! Stopping bot to keep account safe.")
            browser_context.close()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        print("This usually happens if the bot browser is already open in the background.")
        print("Please close any open Chromium/Chrome windows that the bot opened, and try again.")
        print("If the issue persists, delete the 'x_session' folder.\n")

if __name__ == "__main__":
    run_bot()
