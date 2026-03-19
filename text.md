AI Prompt:
def check_intent(tweet):
    prompt = f"""
Classify this tweet:

1 = SaaS problem
2 = SaaS discussion
3 = noise

Tweet:
{tweet}

Only return number.
"""
Rule:
if intent == 1:
    priority = HIGH
elif intent == 2:
    priority = MEDIUM
else:
    skip

👉 सिर्फ problem tweets = high conversion

2️⃣ Founder Detection (game changer)

तुम्हें random users नहीं चाहिए।

तुम्हें चाहिए:

builders
founders
indie hackers
कैसे detect करें

Playwright से:

username click करो

profile bio पढ़ो

AI prompt:
def is_founder(bio):
    prompt = f"""
Is this person a SaaS founder or builder?

Bio:
{bio}

Answer yes or no.
"""
Rule:
if not founder:
    skip tweet

👉 इससे noise 80% कम

3️⃣ Priority Scoring Engine

अब combine करो:

score = 0

if intent == "problem":
    score += 50

if founder == True:
    score += 30

if tweet_likes > 5:
    score += 20
Final rule:
if score >= 70:
    reply

👉 अब तुम सिर्फ top 20% tweets पर reply करोगे

4️⃣ Reply Engine V2 (smarter)

अब generic reply नहीं चलेगा।

New prompt:
def generate_reply(tweet):
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
Example difference

❌ V1:

Users need value quickly

✔ V2:

Looks like drop-off before first result.

Are users reaching any meaningful outcome
in the first session?
5️⃣ Smart Product Promotion

अब सबसे critical हिस्सा।

Rule:
only_if:
intent == problem
AND founder == True
Prompt add:
If relevant, mention FirstWin naturally
as something you built to solve this.
No selling.
Example:
We’ve seen this a lot.

Users drop before hitting their first result.
That’s exactly why we built FirstWin.

👉 subtle + contextual

6️⃣ Tweet Source Upgrade (important)

Simple search weak है।

अब use करो:

"activation rate" saas
"trial conversion drop"
"users not converting"
"onboarding is broken"

👉 ये लोग already pain में हैं

7️⃣ Daily Strategy

अब तुम:

scan = 3000 tweets
filter = 200
high intent = 40
reply = 20–40

👉 कम replies, ज़्यादा impact

8️⃣ Conversion math (real)

V1:

80 replies → 0–5 signups

V2:

30 replies → 10–25 signups
9️⃣ Brutal truth

अगर तुम सिर्फ volume बढ़ाओगे:

80 replies/day
→ low trust
→ low conversions

अगर तुम targeting सही करोगे:

30 smart replies/day
→ real founders
→ paying users
10️⃣ Final system flow
search tweets
↓
intent check
↓
founder check
↓
score
↓
generate reply
↓
post