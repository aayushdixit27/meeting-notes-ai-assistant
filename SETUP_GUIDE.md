# Setup Guide for Meeting Notes AI Assistant

## Quick Start (5 minutes)

### Step 1: Get Your API Key
1. Go to https://console.anthropic.com/
2. Sign up for an account (if you don't have one)
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy the key (it looks like: `sk-ant-...`)

### Step 2: Set Up Your Environment
1. Open Terminal and navigate to this project folder:
```bash
cd "/Users/aayushdixit/Downloads/Mini AI Assistant for Meeting Notes"
```

2. Create a `.env` file with your API key:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```
(Replace `your_key_here` with your actual API key)

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have pip installed:
- macOS: `python3 -m ensurepip --upgrade`
- Windows: Download Python from python.org (pip comes included)

### Step 4: Run the App
```bash
python app.py
```

### Step 5: Open in Browser
Visit: http://localhost:5000

That's it! You're ready to analyze meeting notes.

---

## Testing the App

### Option 1: Use the Example Meeting Notes
1. Open `example_meeting_notes.txt` in this folder
2. Copy all the text
3. Paste it into the web interface
4. Click "Summarize Meeting"

### Option 2: Use Your Own Meeting Notes
- Paste any meeting transcript (minimum 50 characters)
- Works best with 500-5000 words
- Can handle up to ~150,000 words (but that's expensive!)

---

## Understanding What You Built

### The Architecture
```
User Browser (Frontend)
    ↓ [HTTP Request]
Flask Server (Backend)
    ↓ [API Call]
Claude AI (External Service)
    ↓ [AI Response]
Flask Server (Backend)
    ↓ [HTTP Response]
User Browser (Frontend)
```

### The Files and What They Do

**app.py** - The main application
- Handles HTTP requests from the browser
- Routes like `/summarize` and `/summaries`
- Coordinates between frontend and Claude API

**claude_client.py** - API integration
- Talks to Claude's API
- Handles errors (rate limits, network issues)
- Tracks costs and performance

**templates/index.html** - The user interface
- The webpage users interact with
- JavaScript handles form submission
- Displays results dynamically

**static/style.css** - Visual styling
- Makes the app look good
- Responsive design for different screen sizes

**data/summaries.json** - Data storage
- Stores all meeting summaries
- Gets created automatically when you first use the app

---

## PM Learning Exercises

### Exercise 1: Understand Latency
1. Open Browser DevTools (F12)
2. Go to Network tab
3. Submit a meeting summary
4. Watch the `/summarize` request
5. Note the time it takes

**Questions to think about:**
- How long did the API call take?
- How would this feel if it took 10 seconds? 30 seconds?
- What's an acceptable wait time for users?

### Exercise 2: Track Costs
1. Summarize a short meeting (500 words)
2. Note the "Estimated Cost" in the results
3. Summarize a long meeting (2000 words)
4. Compare the costs

**Questions to think about:**
- If 1000 users each summarize 5 meetings/day, what's the monthly cost?
- At what scale does this become expensive?
- How would you optimize costs?

### Exercise 3: Test Error Handling
1. Try submitting empty notes (should show error)
2. Try submitting very short notes (should show error)
3. Turn off your internet and try (should show connection error)

**Questions to think about:**
- What errors are handled gracefully?
- What happens if the API key is wrong?
- How would you improve error messages?

### Exercise 4: Explore Rate Limits
1. Click "Summarize" multiple times quickly
2. Observe what happens

**Questions to think about:**
- How many requests can you make per minute?
- What would happen with 100 concurrent users?
- How would you implement a queue system?

### Exercise 5: Monitor Context Windows
1. Look at the "Input Tokens" in results
2. Try longer and longer meetings
3. Calculate what percentage of the context window you're using

**Questions to think about:**
- Claude has a 200K token limit - how much are you using?
- What happens if someone pastes a 200-page document?
- How would you handle very long meetings?

---

## Common Issues and Solutions

### "ANTHROPIC_API_KEY not found"
- Make sure you created the `.env` file
- Check that there are no typos in the key
- Ensure the `.env` file is in the project root directory

### "Rate limit exceeded"
- You're making too many requests too fast
- Anthropic has usage limits on free tier
- Wait a minute and try again
- Consider upgrading your API plan

### "Connection refused" or "Cannot connect"
- Check your internet connection
- Verify the Claude API is accessible (check status.anthropic.com)
- Try again in a few moments

### "Module not found" errors
- Make sure you ran `pip install -r requirements.txt`
- Try `pip3` instead of `pip`
- Check that you're using Python 3.8+

### Port 5000 already in use
- Another app is using port 5000
- Change the port in app.py (last line): `app.run(debug=True, port=5001)`

---

## What to Build Next

### Beginner Extensions
1. **Add a character counter** - Show how many characters/words before submitting
2. **Save/download summaries** - Add a download button for each summary
3. **Dark mode** - Toggle between light and dark themes

### Intermediate Extensions
1. **File upload** - Let users upload .txt or .docx files instead of copy-paste
2. **Action items extraction** - Pull out specific action items and deadlines
3. **Multi-meeting comparison** - Compare multiple meetings side by side

### Advanced Extensions
1. **Speaker identification** - Parse and track who said what
2. **Email integration** - Auto-forward meeting notes via email
3. **Slack bot** - Post summaries directly to Slack
4. **Real-time processing** - Summarize meeting notes as they're being typed

---

## PM Concepts Learned

By building this project, you've experienced:

1. **API Integration** - How products communicate with external services
2. **Rate Limiting** - Why APIs have usage caps and how to handle them
3. **Error Handling** - What happens when things go wrong
4. **Latency** - How response time affects user experience
5. **Cost Management** - How AI features translate to real costs
6. **Context Windows** - Input size limitations and their impact
7. **Prompt Engineering** - How to craft effective AI requests
8. **Data Persistence** - How to save and retrieve user data
9. **Frontend/Backend Split** - How web applications are architected
10. **Monitoring** - How to track performance and usage

---

## Next Steps

1. **Experiment** - Try different types of meeting notes, vary the length
2. **Break it** - Intentionally cause errors to see how the app handles them
3. **Measure** - Track costs and performance over multiple uses
4. **Extend** - Add a new feature from the suggestions above
5. **Share** - Show someone what you built and explain how it works

---

## Resources for Learning More

### APIs and Web Development
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTTP Status Codes Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Best Practices](https://restfulapi.net/)

### AI and Claude
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Token Counting](https://docs.anthropic.com/claude/docs/models-overview)

### Product Management
- [Measuring Latency](https://web.dev/rail/)
- [Calculating API Costs](https://openai.com/pricing) (compare different providers)
- [Error Handling UX](https://www.nngroup.com/articles/error-message-guidelines/)

---

## Questions?

If you run into issues or want to understand something better:
1. Read the code comments (they're written for learning!)
2. Check the PM insights throughout the code
3. Try the debugging exercises above
4. Experiment and see what happens

Remember: Breaking things is how you learn. This is a safe environment to experiment!

Happy building! 🚀
