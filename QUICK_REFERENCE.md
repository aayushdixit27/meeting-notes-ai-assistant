# Quick Reference Card

## Setup (First Time Only)

```bash
# 1. Get API key from https://console.anthropic.com/
# 2. Create .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Or use the quick start script:
```bash
./start.sh
```

## Starting the App

```bash
python app.py
```

Then open: http://localhost:5000

## Project Structure (Quick Glance)

```
app.py              → Web server (routes, API endpoints)
claude_client.py    → Claude API integration
templates/          → HTML frontend
static/             → CSS styling
data/               → Stored summaries
```

## Key Endpoints

- `GET /` → Main page
- `POST /summarize` → Analyze meeting notes
- `GET /summaries` → Get past summaries
- `GET /health` → Health check

## Claude API Quick Facts

**Model:** Claude 3.5 Sonnet
**Context:** 200K tokens (~150K words)
**Pricing:**
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens

**Average meeting (1000 words):**
- Cost: ~$0.008
- Time: 2-5 seconds
- Tokens: ~1,300 input + ~300 output

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Check Python version
python --version

# View environment variables
cat .env

# View stored summaries
cat data/summaries.json

# Clear all summaries
rm data/summaries.json
```

## Rate Limits (Typical Free Tier)

- Requests per minute: 50
- Tokens per minute: 40,000
- Concurrent requests: 5

Check your limits at: https://console.anthropic.com/

## PM Metrics Cheat Sheet

**Latency (Response Time):**
- Good: < 2 seconds
- Acceptable: 2-5 seconds
- Slow: > 5 seconds

**Cost per User (Monthly):**
```
users × meetings/day × days × avg_cost
Example: 100 × 1 × 30 × $0.008 = $24/month
```

**Context Window Usage:**
```
(tokens_used / 200000) × 100 = percentage
Example: (1300 / 200000) × 100 = 0.65%
```

## Error Codes

- `400` → Bad input (fix your request)
- `401` → Bad API key (check .env)
- `429` → Rate limited (slow down)
- `500` → Server error (check logs)
- `503` → API down (wait and retry)

## File Sizes

**Small meeting:** 500 words → ~$0.005
**Medium meeting:** 2,000 words → $0.015
**Large meeting:** 5,000 words → $0.035
**Huge meeting:** 20,000 words → $0.140

## Debugging Checklist

❌ **App won't start?**
- Check Python version (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is free

❌ **API errors?**
- Check .env file exists
- Verify API key is correct
- Check internet connection

❌ **Slow responses?**
- Check meeting size (too long?)
- Check network latency
- Check Claude API status

❌ **Bad summaries?**
- Try different wording in notes
- Check input is clear and structured
- Verify enough content (>50 chars)

## Quick Test

Use this sample meeting:
```
Team sync 10/23
Sarah: Let's review Q4 goals
Mike: On track for feature launch
Action: Submit proposal by Friday
```

Should return:
- Summary with bullet points
- Sentiment (probably Neutral/Positive)
- Topics and keywords

## Browser DevTools (F12)

**Network Tab:**
- See API calls in real-time
- Check request/response times
- Debug errors

**Console Tab:**
- See JavaScript logs
- Debug frontend issues

**Application Tab:**
- View stored data
- Check cookies/storage

## PM Questions to Practice

While using the app, ask yourself:

1. How long did that take? (latency)
2. How much did it cost? (economics)
3. What if it failed? (error handling)
4. What if 1000 people did this? (scale)
5. How would I explain this to users? (UX)

## Vocabulary Builder

**API** → How programs talk to each other
**Endpoint** → Specific URL for an API function
**Token** → Unit of text for AI (≈0.75 words)
**Latency** → Time between request and response
**Rate limit** → Max requests per time period
**Context window** → How much text AI can see
**Prompt** → Instructions you give to AI
**Webhook** → API that calls you back
**REST** → Common API design pattern
**JSON** → Data format for API responses

## Cost Calculator

```python
# Per summary
input_tokens = word_count * 1.3
output_tokens = 300  # typical summary
cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)

# Per month
monthly_cost = cost × meetings_per_day × days_per_month × users
```

## Extension Ideas (by Difficulty)

**Easy (1 hour):**
- Add word counter
- Change color scheme
- Add more example meetings

**Medium (1 day):**
- File upload
- Download summary as PDF
- Search past summaries

**Hard (1 week):**
- User authentication
- Real-time collaboration
- Slack integration

## Resources

**Documentation:**
- Flask: https://flask.palletsprojects.com/
- Claude: https://docs.anthropic.com/
- Python: https://docs.python.org/

**Tools:**
- API key: https://console.anthropic.com/
- Token counter: https://www.anthropic.com/claude/tokenizer

**Learning:**
- PM concepts: Read PM_CONCEPTS.md
- Setup help: Read SETUP_GUIDE.md
- Architecture: Read PROJECT_SUMMARY.md

## One-Liners

```bash
# Fresh start (remove all data)
rm data/summaries.json && python app.py

# Check if app is running
curl http://localhost:5000/health

# Count summaries stored
cat data/summaries.json | grep "title" | wc -l

# View latest summary
cat data/summaries.json | python -m json.tool | head -30

# Install in virtual environment
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Quick test
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{"notes": "Quick test meeting. Discussed project status. All good.", "title": "Test"}'
```

## Troubleshooting Speed Guide

| Problem | Quick Fix |
|---------|-----------|
| API key error | Check .env file |
| Slow response | Check meeting size |
| Rate limited | Wait 1 minute |
| Won't start | Check port 5000 |
| Bad summary | Improve input |
| High costs | Use shorter inputs |

## Remember

- **Every click = a cost** (but tiny!)
- **Every wait = bad UX** (optimize latency)
- **Every error = learning** (read the message)
- **Every feature = trade-offs** (cost vs. value)

---

**Quick Start:** `./start.sh` → http://localhost:5000 → paste meeting → click Summarize

**Need Help?** Read SETUP_GUIDE.md or PM_CONCEPTS.md

**Want to Learn?** Try breaking things intentionally!
