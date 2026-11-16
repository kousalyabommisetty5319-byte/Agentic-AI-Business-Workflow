import requests
import json

# =====================================
# AGENTIC AI CUSTOMER ENQUIRY SYSTEM
# =====================================

MODEL = "llama3.2"

OLLAMA_URL = "http://localhost:11434/api/chat"


# =====================================
# STEP 1: CUSTOMER INFORMATION
# =====================================

customer_name = input("Enter Customer Name: ")

customer_id = input("Enter Customer ID: ")

message = input("Enter Customer Enquiry: ")


# =====================================
# STEP 2: AI DECISION ENGINE
# =====================================

def analyze_enquiry(customer_name, customer_id, message):

    prompt = f"""
    You are an intelligent customer support AI agent.

    Customer Name: {customer_name}
    Customer ID: {customer_id}

    Customer Enquiry:
    {message}

    Analyze the enquiry and return ONLY valid JSON.

    Use this structure:

    {{
        "category": "Enquiry category",
        "problem": "Explain the customer's problem",
        "priority": "High, Medium or Low",
        "decision": "Next appropriate action",
        "response": "Professional customer response"
    }}

    Rules:
    1. Use the actual customer name.
    2. Never invent order status or transaction details.
    3. Do not claim that an action has been completed.
    4. If information is missing, request clarification.
    5. Keep the response professional.
    """

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "format": "json",
        "stream": False
    }

    try:

        result = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        result.raise_for_status()

        response = result.json()

        ai_output = response["message"]["content"]

        return json.loads(ai_output)

    except requests.exceptions.RequestException as error:

        print("LLM connection error:", error)

        return None

    except (KeyError, json.JSONDecodeError):

        print("Invalid AI response.")

        return None


# =====================================
# STEP 3: DISPLAY AI ANALYSIS
# =====================================

print("\n===================================")
print("       AI ANALYSIS RESULTS")
print("===================================")

analysis = analyze_enquiry(
    customer_name,
    customer_id,
    message
)

if analysis is None:

    print("Unable to process enquiry.")

else:

    print("Customer:", customer_name)

    print("Customer ID:", customer_id)

    print("Category:", analysis["category"])

    print("Problem:", analysis["problem"])

    print("Priority:", analysis["priority"])

    print("AI Decision:", analysis["decision"])


    # =================================
    # STEP 4: GENERATE RESPONSE
    # =================================

    print("\n===================================")
    print("       GENERATED RESPONSE")
    print("===================================")

    print(analysis["response"])


    # =================================
    # STEP 5: HUMAN APPROVAL
    # =================================

    print("\n===================================")
    print("         HUMAN APPROVAL")
    print("===================================")

    approval = input(
        "Approve this response? (yes/no): "
    ).strip().lower()

    if approval == "yes":

        print("\nResponse Approved!")

        print("Final Customer Response:")

        print(analysis["response"])

        print("\nStatus: Approved")

    else:

        print("\nResponse Rejected.")

        print("Status: Pending Revision")
