"""
BHRT Engine -- Usage Examples
==============================

Run this file to see the engine in action with different inputs.
"""

from bhrt_engine import process, to_json

# ----------------------------------------------------------
# Example 1: Professional workplace text (English)
# ----------------------------------------------------------
print("=" * 70)
print("EXAMPLE 1: Professional Workplace Text")
print("=" * 70)

text1 = """
My name is Priya Sharma and I am 28 years old. I work as a project manager
at a tech company in Bangalore. Yesterday, I had a terrible meeting with
my client Mr. Gupta. I felt frustrated and angry because the deadline was
moved again. My phone is +919876543210 and email is priya.s@email.com.
We discussed the project timeline for 3 months. The budget was Rs.25,00,000.
I think we should present the strategy to the team next week.
"""

result1 = process(text1)
print("\n--- Structure Text ---")
print(result1.structure_text)
print("\n--- Behavioral Pattern ---")
print("Pattern:", result1.behavioral_pattern)
print("\n--- Metrics ---")
print("Privacy Score:", result1.privacy_score, "/100")
print("Utility Score:", result1.utility_score, "/100")
print("BHRT Score:", result1.bhrt_score, "/100")
print("Identity tokens removed:", result1.identity_tokens_found)

# ----------------------------------------------------------
# Example 2: Personal emotional text (Hinglish)
# ----------------------------------------------------------
print("\n" + "=" * 70)
print("EXAMPLE 2: Personal Emotional Text (Hinglish)")
print("=" * 70)

text2 = """
Main aaj bahut udaas hoon. Kal mujhe office mein gussa aaya tha.
Mera boss ne mujhe daanta. Maine socha ki shayad meri galti thi.
Mujhe lagta hai main fail ho gaya. Mera phone 9876543210 hai.
Main Mumbai mein rehta hoon. Abhi tak main thak gaya hoon.
"""

result2 = process(text2)
print("\n--- Structure Text ---")
print(result2.structure_text)
print("\n--- Behavioral Pattern ---")
print("Pattern:", result2.behavioral_pattern)
print("\n--- Metrics ---")
print("Privacy Score:", result2.privacy_score, "/100")
print("Utility Score:", result2.utility_score, "/100")
print("BHRT Score:", result2.bhrt_score, "/100")
print("Language detected:", result2.language_detected)

# ----------------------------------------------------------
# Example 3: Minimal text
# ----------------------------------------------------------
print("\n" + "=" * 70)
print("EXAMPLE 3: Minimal Text")
print("=" * 70)

text3 = "I am happy today and I love my work."
result3 = process(text3)
print("\n--- Structure Text ---")
print(result3.structure_text)
print("\n--- Topic Distribution ---")
for topic, score in result3.topic_distribution.items():
    print("  ", topic, ":", score)

# ----------------------------------------------------------
# Example 4: Full JSON output
# ----------------------------------------------------------
print("\n" + "=" * 70)
print("EXAMPLE 4: Full JSON Output (truncated)")
print("=" * 70)

json_output = to_json(result1)
print(json_output[:800] + "...")

print("\n" + "=" * 70)
print("All examples completed successfully!")
print("=" * 70)