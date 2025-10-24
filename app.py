"""
Meeting Notes AI Assistant - Main Application

This is a Flask web application that demonstrates how AI APIs work in practice.
Perfect for Product Managers learning about AI integration.

PM Learning Focus:
- How APIs handle requests and responses
- Error handling in production
- Data persistence
- Cost tracking
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from claude_client import ClaudeClient, check_context_window

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Path to store summaries
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SUMMARIES_FILE = os.path.join(DATA_DIR, 'summaries.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def load_summaries() -> list:
    """
    Load saved summaries from disk.

    PM Insight: In production, you'd use a real database (PostgreSQL, MongoDB, etc.)
    For learning purposes, we're using a JSON file - it's simple and readable.
    """
    if not os.path.exists(SUMMARIES_FILE):
        return []

    try:
        with open(SUMMARIES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_summary(summary_data: dict):
    """
    Save a new summary to disk.

    PM Insight: This is called a "write operation." In production, you'd think about:
    - What if multiple users write at once? (concurrency)
    - What if the disk is full? (error handling)
    - How do we back this up? (data durability)
    """
    summaries = load_summaries()
    summaries.insert(0, summary_data)  # Add to beginning

    # Keep only last 100 summaries to prevent file from growing too large
    # PM Insight: This is a "data retention policy" - common in production systems
    summaries = summaries[:100]

    with open(SUMMARIES_FILE, 'w') as f:
        json.dump(summaries, f, indent=2)


@app.route('/')
def index():
    """
    Serve the main page.

    PM Insight: This is called a "route" or "endpoint."
    When users visit your-domain.com/, Flask calls this function.
    """
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to summarize meeting notes.

    PM Insight: This is a POST endpoint - it receives data, processes it,
    and returns results. This is the core of most web applications.

    The flow:
    1. User submits form (frontend)
    2. JavaScript makes HTTP POST request (frontend)
    3. Flask receives request (backend - we are here)
    4. We call Claude API (external service)
    5. We return results (backend)
    6. JavaScript displays results (frontend)
    """
    try:
        # Get data from request
        data = request.get_json()

        if not data or 'notes' not in data:
            return jsonify({
                'error': 'Missing meeting notes'
            }), 400  # 400 = Bad Request

        notes = data['notes'].strip()
        title = data.get('title', 'Untitled Meeting')
        include_topics = data.get('includeTopics', True)

        # Validate input
        if len(notes) < 50:
            return jsonify({
                'error': 'Meeting notes too short. Please provide at least 50 characters.'
            }), 400

        # Check context window
        # PM Insight: Always validate before making expensive API calls
        context_check = check_context_window(notes)

        if not context_check['fits']:
            return jsonify({
                'error': f"Meeting notes too long. Estimated {context_check['estimated_tokens']} tokens, "
                        f"but maximum is {context_check['max_tokens']}. "
                        f"Try splitting into smaller chunks."
            }), 400

        if context_check['warning']:
            # PM Insight: We could warn the user, but let's just log it
            print(f"⚠️  Large input: {context_check['percentage_used']}% of context window")

        # Initialize Claude client
        # PM Insight: This could fail if API key is missing or invalid
        try:
            client = ClaudeClient()
        except ValueError as e:
            return jsonify({
                'error': 'API key not configured. Please set ANTHROPIC_API_KEY in .env file. '
                        'Get your key at https://console.anthropic.com/'
            }), 500  # 500 = Internal Server Error

        # Call Claude API
        # PM Insight: This is the actual AI magic happening
        result = client.summarize_meeting(notes, include_topics)

        # Add title and timestamp
        result['title'] = title
        result['timestamp'] = datetime.now().isoformat()

        # Save to disk
        # PM Insight: We do this async in production so API response isn't delayed
        save_summary({
            'title': title,
            'summary': result['summary'],
            'sentiment': result['sentiment'],
            'topics': result.get('topics'),
            'timestamp': result['timestamp']
        })

        # Return success response
        return jsonify(result), 200  # 200 = Success

    except Exception as e:
        # PM Insight: Always log errors in production for debugging
        print(f"❌ Error in /summarize: {str(e)}")

        # Return user-friendly error message
        # PM Insight: Never expose internal error details to users (security risk)
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/summaries', methods=['GET'])
def get_summaries():
    """
    API endpoint to get all saved summaries.

    PM Insight: This is a GET endpoint - it only retrieves data, doesn't modify anything.
    GET requests should be "idempotent" (same result every time, no side effects).
    """
    try:
        summaries = load_summaries()
        return jsonify(summaries), 200

    except Exception as e:
        print(f"❌ Error in /summaries: {str(e)}")
        return jsonify({
            'error': 'Failed to load summaries'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    PM Insight: Production systems always have health check endpoints.
    Monitoring services (like Datadog, New Relic) ping this to ensure app is running.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(_error):
    """
    Handle 404 errors (page not found).

    PM Insight: Good error handling improves user experience.
    Users should never see cryptic error messages.
    """
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors (server errors).

    PM Insight: When things go wrong, fail gracefully.
    Log the details for debugging, but show users a friendly message.
    """
    print(f"❌ Internal error: {str(error)}")
    return jsonify({
        'error': 'Internal server error. Please try again later.'
    }), 500


if __name__ == '__main__':
    """
    Run the Flask development server.

    PM Insight: This is for development only. In production, you'd use:
    - Gunicorn or uWSGI (production web servers)
    - Nginx (reverse proxy)
    - Docker (containerization)
    - AWS/GCP/Azure (hosting)

    But for learning, this simple server is perfect!
    """
    print("🚀 Starting Meeting Notes AI Assistant...")
    print("📝 Open http://localhost:5001 in your browser")
    print("🧠 Make sure your ANTHROPIC_API_KEY is set in .env file")
    print("\n💡 PM Tip: Open browser DevTools (F12) > Network tab to see API calls in action!\n")

    # Run Flask app
    # debug=True enables auto-reload when you change code
    # PM Insight: Never use debug=True in production (security risk)
    app.run(debug=True, host='0.0.0.0', port=5001)
