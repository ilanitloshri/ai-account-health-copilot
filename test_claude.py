# test_claude.py
# Sends one question to Claude and prints the answer, token counts and cost.

import os

import anthropic
from dotenv import load_dotenv

# Read the API key from the .env file
load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("No ANTHROPIC_API_KEY found. Add it to the .env file.")
    raise SystemExit

# Model and its prices (US dollars per 1 million tokens)
MODEL = "claude-opus-5-5"
INPUT_PRICE_PER_MILLION = 4.00
OUTPUT_PRICE_PER_MILLION = 20.00

PROMPT = (
    "In two sentences: what is the single best early warning sign "
    "that an enterprise customer of an AI platform might not renew?"
)

# Connect to Claude (the key is picked up automatically)
client = anthropic.Anthropic()

# Send the question
response = client.beta.messages.create(
    model=MODEL,
    max_tokens=16000,
    messages=[{"role": "user", "content": PROMPT}],
    # If Claude's safety filter declines, retry on a backup model automatically
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",
)

# Print the answer
if response.stop_reason == "refusal":
    print("Claude declined to answer this prompt.")
else:
    for block in response.content:
        if block.type == "text":
            print("ANSWER:")
            print(block.text)

# Count tokens and work out the cost
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
cost = (input_tokens * INPUT_PRICE_PER_MILLION
        + output_tokens * OUTPUT_PRICE_PER_MILLION) / 1_000_000

print()
print(f"Model used:    {response.model}")
print(f"Input tokens:  {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Cost:          ${cost:.6f}")
