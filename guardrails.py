import re

# 5.2 Refusal Logic
REFUSAL_MESSAGE = (
    "I am a facts-only assistant and cannot provide investment advice, "
    "recommendations, or opinions on which fund is better."
)

# 5.3 Educational Redirection
EDUCATIONAL_LINK = "\n\nFor educational resources on mutual fund investing, please visit AMFI: https://www.amfiindia.com/investor-corner"

# 5.1 Intent Classification
# We use a lightweight rule-based (regex) approach for fast intent classification
ADVISORY_PATTERNS = [
    r"should i invest",
    r"should i buy",
    r"which (fund )?is better",
    r"which (fund )?is best",
    r"recommend",
    r"advice",
    r"good investment",
    r"bad investment",
    r"what should i buy",
    r"is it good to",
    r"compare .* (and|with) ",
    r"better return",
    r"where to invest",
    r"is it safe to invest",
    r"portfolio review"
]

def is_advisory_query(query: str) -> bool:
    """Checks if a query is asking for financial advice or opinions."""
    query_lower = query.lower()
    for pattern in ADVISORY_PATTERNS:
        if re.search(pattern, query_lower):
            return True
    return False

def handle_query_guardrails(query: str):
    """
    Evaluates the query against guardrails.
    Returns a refusal response if the query is advisory, otherwise returns None.
    """
    if is_advisory_query(query):
        return REFUSAL_MESSAGE + EDUCATIONAL_LINK
    return None

if __name__ == "__main__":
    print("\n--- Testing Guardrails ---")
    test_queries = [
        "What is the expense ratio?",
        "Should I invest in HDFC Mid-Cap?",
        "Which fund is better between small cap and mid cap?",
        "Minimum SIP amount for tax saver fund."
    ]
    
    for q in test_queries:
        print(f"Query: '{q}'")
        refusal = handle_query_guardrails(q)
        if refusal:
            print(f"Result: BLOCKED -> {refusal}\n")
        else:
            print("Result: PASSED\n")
