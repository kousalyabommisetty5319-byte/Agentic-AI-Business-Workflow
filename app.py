from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


@app.route("/analyze", methods=["POST"])
def analyze_enquiry():

    try:
        data = request.get_json()

        customer_name = data.get("customer_name", "Customer")
        customer_id = data.get("customer_id", "Not provided")
        message = data.get("message", "")

        if not message.strip():
            return jsonify({"error": "Customer enquiry is required"}), 400

        prompt = f"""
You are a professional customer support AI agent.

Customer Name: {customer_name}
Customer ID: {customer_id}
Customer Enquiry: {message}

Analyze the enquiry and return ONLY valid JSON.

Use these exact fields:
{{
    "category": "Enquiry category",
    "problem": "Customer problem",
    "priority": "High, Medium, or Low",
    "decision": "Recommended next action",
    "response": "Professional response to the customer"
}}

Rules:
- Use the actual customer name.
- Never invent phone numbers, email addresses or contact details.
- Never include phone numbers, email addresses, or links in the decision or response.
- Recommend human review without claiming that a refund or replacement is being processed.
- Never invent order status or refund status.
- Never promise that a refund has been processed.
- Never claim an action has already been completed.
- Do not invent company policies.
- If information is missing, ask the customer for it.
- Recommend human review before taking action.
- Be polite and professional.
- Set priority to High for damaged products, refund requests, missing orders, or serious customer complaints.
- Set priority to Medium for general complaints or delayed responses.
- Set priority to Low for simple questions or general information requests.
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "format": "json",
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        ai_output = json.loads(result["message"]["content"])

        return jsonify({
            "customer_name": customer_name,
            "customer_id": customer_id,
            "category": ai_output["category"],
            "problem": ai_output["problem"],
            "priority": ai_output["priority"],
            "decision": ai_output["decision"],
            "response": ai_output["response"],
            "approval_status": "Pending Human Approval"
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Could not connect to Ollama.",
            "details": str(e)
        }), 503

    except Exception as e:
        return jsonify({
            "error": "Something went wrong.",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)