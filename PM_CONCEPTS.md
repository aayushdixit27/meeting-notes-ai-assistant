# PM Concepts Deep Dive

This document explains the technical concepts you've just built, from a Product Manager's perspective.

---

## 1. What is an API Call?

### The Restaurant Analogy
Think of an API like a restaurant:
- **You (the customer)** = Your app's frontend
- **The waiter** = The API
- **The kitchen** = Claude's AI servers

You don't go into the kitchen and cook. You tell the waiter what you want, the waiter tells the kitchen, the kitchen prepares it, and the waiter brings it back to you.

### What Actually Happens
```
1. Your frontend makes an HTTP POST request
   ↓
2. Request travels over the internet to Anthropic's servers
   ↓
3. Anthropic's servers authenticate your API key
   ↓
4. Claude AI processes your prompt (this takes a few seconds)
   ↓
5. Response travels back over the internet
   ↓
6. Your frontend displays the result
```

### Why This Matters for PMs
- **You can't control the kitchen** - If Claude is slow or down, your app is affected
- **You pay per order** - Every API call costs money (based on tokens)
- **There's a limit** - You can't make infinite requests (rate limits)
- **Quality varies** - Sometimes the AI gives better results than other times

---

## 2. Rate Limits: Why APIs Say "Slow Down"

### What Are Rate Limits?
Anthropic (and all API providers) limit how many requests you can make:
- **Requests Per Minute (RPM)** - e.g., 50 requests per minute
- **Tokens Per Minute (TPM)** - e.g., 40,000 tokens per minute
- **Concurrent Requests** - e.g., 5 simultaneous requests

### The Highway Analogy
Imagine the API is a highway:
- Rate limits are like **speed limits and lane restrictions**
- They prevent one person from hogging all the lanes
- They ensure everyone gets a fair share of the road
- They protect the infrastructure from overload

### Real-World Scenario
You have 100 users who all click "Summarize" at the same time:

**Without rate limiting:**
- All 100 requests hit Claude simultaneously
- Your API key might get throttled
- Some requests fail, users see errors
- Bad user experience

**With good rate limiting handling:**
- You implement a queue system
- First 50 requests go through immediately
- Next 50 wait in queue
- Users see "Position 23 in queue..."
- Much better experience

### PM Decisions You'll Face
1. **Do we queue or fail fast?**
   - Queue = Better UX, more complex engineering
   - Fail fast = Simpler, but frustrating for users

2. **Do we upgrade our API plan?**
   - Higher limits cost more money
   - But might be worth it for user experience

3. **Can we batch requests?**
   - Instead of 100 separate calls, can we combine them?
   - This is common for things like image processing

---

## 3. Error Handling: When Things Go Wrong

### Types of Errors You'll Encounter

#### 400 Bad Request
**What it means:** The user sent invalid data
**Example:** Empty meeting notes, notes too short
**PM Decision:** Write clear error messages that help users fix the problem

#### 401 Unauthorized
**What it means:** API key is missing or invalid
**Example:** Forgot to set up .env file
**PM Decision:** Good onboarding docs prevent this

#### 429 Rate Limited
**What it means:** Too many requests too fast
**Example:** User clicks "Summarize" 20 times in 10 seconds
**PM Decision:** Disable button after click, implement queue, or upgrade plan

#### 500 Internal Server Error
**What it means:** Something broke on your server
**Example:** Database connection failed, bug in code
**PM Decision:** Monitor these closely, set up alerts, fix ASAP

#### 503 Service Unavailable
**What it means:** Claude's API is down or overloaded
**Example:** Claude is having an outage
**PM Decision:** Have a maintenance page, status updates, fallback plan

### The User Experience of Errors

**Bad Error Message:**
```
Error: HTTP 429
```

**Good Error Message:**
```
We're receiving a lot of requests right now.
Your summary will be ready in about 30 seconds.
[Progress bar showing position in queue]
```

### PM Question: How Much Should We Tell Users?

**Too little:**
- "An error occurred"
- Users have no idea what to do

**Too much:**
- "APIConnectionError: Failed to establish connection to api.anthropic.com:443. SSL certificate verification failed..."
- Confusing and potentially reveals security info

**Just right:**
- "We couldn't connect to our AI service. Please check your internet connection and try again."
- Clear, actionable, no technical jargon

---

## 4. Cost Per Call: The Economics of AI

### How Pricing Works

Claude charges by **tokens** (roughly 0.75 words = 1 token):
- **Input tokens:** What you send to Claude
- **Output tokens:** What Claude sends back

Current pricing (Claude 3.5 Sonnet):
- Input: $3 per million tokens
- Output: $15 per million tokens

### Real Cost Examples

**Small meeting summary (500 words):**
- Input: ~650 tokens = $0.00195
- Output: ~200 tokens = $0.003
- **Total: ~$0.005 per summary**

**Large meeting summary (2000 words):**
- Input: ~2,600 tokens = $0.0078
- Output: ~400 tokens = $0.006
- **Total: ~$0.014 per summary**

### Scaling Calculations

**Scenario: 10,000 users, each summarizes 5 meetings/week**

Assumptions:
- Average meeting: 1000 words (1,300 tokens input)
- Average summary: 300 tokens output

Math:
- 10,000 users × 5 meetings = 50,000 summaries/week
- 50,000 × 1,300 tokens = 65,000,000 input tokens
- 50,000 × 300 tokens = 15,000,000 output tokens

Cost per week:
- Input: 65M × $3/1M = $195
- Output: 15M × $15/1M = $225
- **Total: $420/week = ~$1,680/month**

### PM Decisions

1. **Is this feature worth the cost?**
   - If we charge $10/month per user, 10,000 users = $100k revenue
   - AI costs = $1,680/month (1.68% of revenue)
   - Yes, totally worth it!

2. **Should we limit usage?**
   - Free tier: 10 summaries/month
   - Paid tier: Unlimited
   - This controls costs while encouraging upgrades

3. **Can we optimize?**
   - Use a smaller, cheaper model for simple tasks
   - Cache common queries
   - Compress input (remove unnecessary words)

4. **How do we price this feature?**
   - Cost-plus: AI costs $0.005, we charge $0.10 (20x markup)
   - Value-based: Users save 30 min/meeting, charge based on time saved
   - Bundled: Include in subscription, average out costs

---

## 5. Latency: The Psychology of Waiting

### What is Latency?
**Latency** = The time between when a user takes an action and when they see the result

In our app:
- User clicks "Summarize"
- Latency = Time until they see the summary

### Human Perception of Time

**0.1 seconds:** Feels instant
- Example: Typing, button clicks

**1 second:** Noticeable delay but acceptable
- Example: Page loads, simple queries

**3 seconds:** Getting annoying
- Example: Our AI summaries take about this long
- Users start thinking "Is it working?"

**10 seconds:** Frustrating
- Example: Complex AI tasks, large file uploads
- Users start clicking repeatedly or closing the tab

**30+ seconds:** Unacceptable for most use cases
- Example: Very long AI processing
- Users will leave unless you keep them engaged

### Managing User Expectations

**Bad UX:**
```
[User clicks button]
[Nothing happens for 3 seconds]
[Results suddenly appear]
```

**Good UX:**
```
[User clicks button]
[Immediately show spinner]
[Show message: "Claude is analyzing your meeting notes..."]
[Show progress: "This usually takes 2-5 seconds"]
[Results appear]
```

### PM Strategies for High Latency

1. **Show progress indicators**
   - Spinners, progress bars, estimated time
   - Makes wait feel shorter

2. **Give something immediate**
   - Acknowledge the action instantly
   - "Processing..." appears immediately even if AI takes 3 seconds

3. **Set expectations upfront**
   - "Large meetings may take up to 10 seconds"
   - Users are more patient when they know what to expect

4. **Provide entertainment**
   - Fun loading messages
   - Random tips or facts
   - Mini animations

5. **Make it asynchronous**
   - "We'll email you when it's ready"
   - Works for very long processes (minutes/hours)

### The Business Impact of Latency

**Research shows:**
- Amazon found that every 100ms delay costs 1% of sales
- Google found that 500ms delay reduces traffic by 20%
- Users expect pages to load in under 2 seconds

**For our app:**
- 3-second latency is borderline
- If we can get it to 1 second, users will love it
- If it creeps to 10 seconds, users will abandon

---

## 6. Context Windows: The AI's Memory Limit

### What is a Context Window?

The **context window** is how much text an AI can "see" at once.

**Claude 3.5 Sonnet:** 200,000 tokens (~150,000 words)

That's roughly:
- 300 pages of text
- A short novel
- 10-15 hour-long meeting transcripts

### Why There's a Limit

**Technical reason:**
- AI models process text in parallel using transformers
- Longer context = exponentially more compute
- 200K tokens is already MASSIVE compared to older models (which had ~4K)

**Practical reason:**
- Most use cases don't need more
- Longer context = slower processing = higher cost

### Real-World Impact

**Scenario 1: Chat History**
You're building a chatbot. User has a long conversation.
- First 20 messages fit fine
- After 200 messages, you hit the context limit
- Now what?

Options:
1. **Summarize old messages** - Compress history to save space
2. **Truncate** - Drop oldest messages (user loses context)
3. **Smart selection** - Keep only relevant messages

**Scenario 2: Document Analysis**
User wants to analyze a 500-page legal document.
- 500 pages = ~300,000 words = ~400,000 tokens
- That's 2x the context window!

Options:
1. **Split into chunks** - Analyze sections separately
2. **Extract key sections** - Only analyze relevant parts
3. **Use a larger model** - Some models have 1M+ token windows (but cost more)

### PM Decisions

1. **Do we tell users about limits?**
   - Show "You're using 80% of context" warning?
   - Or handle silently and split automatically?

2. **How do we handle overflow?**
   - Reject with error? (simple but bad UX)
   - Auto-split? (complex but better UX)
   - Offer to summarize? (creative solution)

3. **Do we need a bigger model?**
   - Claude 3.5 Sonnet: 200K context
   - GPT-4 Turbo: 128K context
   - Gemini 1.5 Pro: 2M context (but costs more)

### The Future

Context windows are growing rapidly:
- 2020: 2K-4K tokens was standard
- 2023: 100K-200K became common
- 2024-2025: 1M-2M tokens available
- Future: Maybe unlimited?

**Why this matters for PMs:**
- Features that were impossible 2 years ago are now easy
- "Analyze entire codebases" - used to need clever chunking, now just works
- Your product capabilities can expand without code changes as models improve

---

## 7. Prompt Engineering: Talking to AI

### What is a Prompt?

A **prompt** is the instruction you give to the AI. It's like giving instructions to a very literal intern.

### Bad Prompt
```
Summarize this meeting.

[meeting notes]
```

### Good Prompt
```
You are an AI assistant specialized in analyzing meeting notes.

Please analyze the following meeting transcript and provide:

1. **Summary**: A concise bullet-point summary of the key points discussed (3-7 bullets)
2. **Sentiment Analysis**: Overall sentiment (Positive, Neutral, Negative, or Mixed) with explanation
3. **Topics & Keywords**: Main topics and key keywords

Meeting Notes:
[meeting notes]

Please format your response as JSON with this structure:
{
    "summary": "...",
    "sentiment": {...},
    "topics": {...}
}
```

### Why the Second is Better

1. **Role definition:** "You are an AI assistant specialized in..."
   - Primes the AI to think in that role
   - Like telling a consultant their expertise area

2. **Clear structure:** Numbered list of what you want
   - AI knows exactly what to deliver
   - No guessing

3. **Examples:** "3-7 bullets"
   - Gives concrete targets
   - Prevents too-short or too-long responses

4. **Format specification:** "format as JSON"
   - Makes parsing easy
   - Reduces errors

### Common Prompt Patterns

**Few-shot learning:**
```
Summarize these meeting notes. Here are examples:

Example 1:
Input: [example meeting]
Output: [example summary]

Example 2:
Input: [example meeting]
Output: [example summary]

Now do this one:
Input: [actual meeting]
```

**Chain of thought:**
```
Analyze this meeting. Think step by step:
1. First, identify the main topics
2. Then, extract key decisions
3. Finally, summarize action items
```

**Constraints:**
```
Summarize in exactly 3 bullet points.
Use simple language a 10-year-old could understand.
Focus only on technical decisions, ignore social chat.
```

### PM Considerations

1. **Prompt quality = Output quality**
   - Bad prompt = bad results, no matter how good the model
   - Spend time crafting good prompts
   - Test with different phrasings

2. **Longer prompts = Higher cost**
   - Every word costs tokens
   - But saving 10 words is penny-wise, pound-foolish if quality suffers

3. **Prompts are your competitive advantage**
   - Everyone has access to Claude
   - Your prompts are what make your product unique
   - Guard them like trade secrets

4. **Test extensively**
   - Try prompts on different types of inputs
   - Edge cases matter (very short, very long, weird formats)
   - A/B test prompts to find what works best

---

## 8. Data Persistence: Saving Stuff

### What is Data Persistence?

**Persistence** = Saving data so it survives after the app closes

In our app, we save summaries to `data/summaries.json`

### Storage Options (Simplest → Most Complex)

1. **JSON Files** (what we use)
   - Pros: Simple, human-readable, no setup
   - Cons: Doesn't scale, no concurrent access, no relationships
   - Use for: Prototypes, small apps, config files

2. **SQLite**
   - Pros: Actual database, still simple, built into Python
   - Cons: Single file, limited concurrency
   - Use for: Small-medium apps, mobile apps, embedded systems

3. **PostgreSQL / MySQL**
   - Pros: Real database, scales well, handles concurrency
   - Cons: Requires server, more complex setup
   - Use for: Production apps, multiple servers

4. **MongoDB / DynamoDB**
   - Pros: NoSQL, very flexible schemas, scales horizontally
   - Cons: Different query language, eventual consistency
   - Use for: Large scale, rapidly changing schemas

5. **Redis**
   - Pros: In-memory, super fast, great for caching
   - Cons: Not persistent by default, stores in RAM
   - Use for: Caching, real-time data, sessions

### What PMs Need to Know

**Questions to ask engineers:**

1. **"Where does the data live?"**
   - Local file? Database? Cloud storage?
   - This affects reliability and scaling

2. **"What happens if the app crashes mid-write?"**
   - Data corruption risk?
   - Atomic transactions?

3. **"How do we back up the data?"**
   - Automated backups?
   - Point-in-time recovery?

4. **"How fast can we retrieve it?"**
   - Milliseconds? Seconds?
   - This affects UX

5. **"What happens at 1M users?"**
   - Current solution scale?
   - Migration plan?

### Real-World Scenario

**Your app stores meeting summaries. It's successful! Now what?**

**At 100 users:**
- JSON file works fine
- Keep it simple

**At 10,000 users:**
- JSON file is getting slow
- Time to migrate to PostgreSQL
- Costs: ~$15/month (managed database)

**At 1M users:**
- Need database scaling
- Add read replicas
- Consider sharding
- Costs: ~$1000/month

**PM Decision Points:**
- When do we invest in migration?
- How much downtime is acceptable?
- What's the cost vs. benefit?

---

## 9. Monitoring: Knowing What's Happening

### What is Monitoring?

**Monitoring** = Continuously watching your app to detect problems

Types of monitoring:

1. **Uptime monitoring**
   - Is the app running?
   - Basic: Ping every minute
   - Alert if down for 5 minutes

2. **Performance monitoring**
   - How fast are responses?
   - Track latency over time
   - Alert if > 5 seconds

3. **Error monitoring**
   - What errors are happening?
   - How often?
   - Which users affected?

4. **Usage monitoring**
   - How many requests per minute?
   - Which features most popular?
   - Cost tracking

### Tools

**Free/Simple:**
- UptimeRobot - Basic uptime checks
- Sentry - Error tracking
- Google Analytics - User tracking

**Mid-tier:**
- Datadog - Comprehensive monitoring
- New Relic - Application performance
- LogRocket - Session replay

**Enterprise:**
- Dynatrace - Full observability
- Splunk - Log analysis at scale

### PM Metrics to Track

1. **Availability (Uptime)**
   - Target: 99.9% = 43 minutes downtime/month
   - Each extra "9" costs exponentially more

2. **Latency (Response Time)**
   - P50: Median response time
   - P95: 95th percentile (catches slow requests)
   - P99: 99th percentile (catches worst cases)

3. **Error Rate**
   - Target: < 0.1% of requests fail
   - Spike = something's wrong

4. **API Costs**
   - Daily spend on Claude API
   - Cost per user
   - Alert if > budget

### The On-Call Incident

**3 AM, your phone buzzes:**
```
ALERT: API latency > 10 seconds
Affecting: 500 users
Started: 5 minutes ago
```

**Good monitoring tells you:**
- What's broken (latency)
- When it started (5 min ago)
- Impact (500 users)
- Where to look (API calls)

**Bad monitoring:**
- User emails you: "App is slow"
- You have no idea what's wrong
- Takes hours to debug

---

## 10. The PM Mindset: Technical Empathy

### What You've Learned by Building

You didn't just build an app - you experienced:

1. **The frustration of setup** (API keys, dependencies)
   - Now you understand why onboarding docs matter

2. **The wait for API responses** (latency)
   - Now you understand why loading states matter

3. **The cost of each request** (tokens)
   - Now you understand why engineers push back on "unlimited" features

4. **The brittleness of parsing** (JSON extraction)
   - Now you understand why "it works 99% of the time" isn't good enough

5. **The complexity of error handling** (all the try/catch)
   - Now you understand why "just add a feature" takes weeks

### How This Makes You a Better PM

**Before this project:**
- Engineer: "Adding real-time summaries will increase API costs 10x"
- You: "But users want it..."

**After this project:**
- Engineer: "Adding real-time summaries will increase API costs 10x"
- You: "Let's calculate: Current cost $0.005/summary, real-time would be $0.05/summary. If we process 1M/month, that's $50k vs $5k. Can we batch updates every 30 seconds instead? That would be $0.01/summary = $10k/month."

### The Questions You Can Now Ask

1. **"What's our P95 latency?"** (not just "Is it fast?")
2. **"What happens if we hit the rate limit?"** (not just "Will it work?")
3. **"How much context window do we need?"** (not just "Can it handle long inputs?")
4. **"What's our error rate on API calls?"** (not just "Does it work?")
5. **"How do we handle concurrent requests?"** (not just "Will it scale?")

### Moving Forward

You now have:
- ✅ Hands-on experience with AI APIs
- ✅ Understanding of technical constraints
- ✅ Ability to estimate costs and timelines
- ✅ Vocabulary to talk with engineers
- ✅ Empathy for technical challenges

**Next steps:**
1. Build more projects (see README for ideas)
2. Read engineering docs with new understanding
3. Join technical discussions confidently
4. Make better product decisions

---

## Conclusion

You've gone from "APIs are magic" to "APIs are HTTP requests with costs, limits, and tradeoffs."

That's the difference between a PM who says "just make it work" and one who says "let's find the right balance of speed, cost, and reliability."

Welcome to the world of technical product management. 🚀
