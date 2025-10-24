# Meeting Notes AI Assistant

A hands-on project to learn how AI products are built, designed for Product Managers who want to understand the technical side.

## What This Project Teaches You

### Core Concepts You'll Learn:
- **API Calls**: How your product "talks" to Claude AI
- **Rate Limits**: Why APIs have usage caps and how to handle them
- **Error Handling**: What happens when things go wrong
- **Cost Per Call**: Understanding the economics of AI features
- **Latency**: Response time and why it matters for UX
- **Context Windows**: How much text an AI can process at once
- **Prompt Engineering**: How to ask AI for what you want

## Features

1. **Upload Meeting Notes**: Copy-paste text or upload .txt files
2. **AI Summarization**: Get bullet-point summaries of key points
3. **Sentiment Analysis**: Understand the overall tone (positive/neutral/negative)
4. **Simple Dashboard**: View all your summaries in one place
5. **Topic Tagging**: Automatic keyword extraction (stretch goal)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python app.py
```

4. Open your browser to `http://localhost:5000`

## Project Structure

```
.
├── app.py                 # Main Flask application
├── claude_client.py       # Claude API integration
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── style.css         # Styling
├── data/
│   └── summaries.json    # Stored summaries (auto-created)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## PM Insights: What You're Actually Building

### The API Call
When you click "Summarize", here's what happens:
1. Your text is sent to Claude's API endpoint
2. Claude processes it (using thousands of GPU calculations)
3. A response comes back (usually in 1-5 seconds)
4. We parse and display the results

**PM Insight**: This is why latency matters. Each second feels like forever to users.

### Rate Limits
APIs have limits to prevent abuse:
- Requests per minute (RPM)
- Tokens per minute (TPM)
- Concurrent requests

**PM Insight**: When designing features, you need to consider: "What if 1000 users do this at once?"

### Context Windows
Claude can process ~200,000 tokens (about 150,000 words). But:
- Larger inputs cost more
- Longer processing takes more time
- There's a hard limit

**PM Insight**: This is why chat history sometimes gets "forgotten" - it's cut off to fit the window.

### Cost Structure
AI APIs charge per token (roughly per word):
- Input tokens: What you send
- Output tokens: What you get back
- Different models have different prices

**PM Insight**: A feature that summarizes 100 meetings/day has real, calculable costs.

## How to Extend This

1. **Add file upload**: Let users upload .docx or .pdf files
2. **Action items extraction**: Pull out tasks and deadlines
3. **Speaker identification**: Track who said what
4. **Meeting comparison**: Compare meetings over time
5. **Email integration**: Auto-summarize meeting recordings

## Troubleshooting

### "API Key Invalid"
- Check your .env file has the correct key
- Make sure there are no extra spaces
- Verify the key is active at console.anthropic.com

### "Rate Limit Exceeded"
- You're making too many requests too fast
- Wait a minute and try again
- Consider implementing a queue system

### "Context Window Exceeded"
- Your meeting notes are too long
- Try splitting into smaller chunks
- Summarize in multiple passes

## What Makes This Real PM Learning?

You're not just using AI - you're building with it. You'll understand:
- Why engineers say "it depends" (on rate limits, context size, cost)
- What's hard vs. easy to implement
- Why small model improvements change everything
- How to talk about technical constraints with confidence

Ready to become a technical PM? Let's build!
