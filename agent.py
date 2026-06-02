
import os
from dotenv import load_dotenv
import google.generativeai as genai

from persona.system_prompt import HAWKING_SYSTEM_PROMPT
from rag.retriever import retrieve
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

short_term = ShortTermMemory(max_turns=10)
long_term = LongTermMemory()

FACTS_TO_REMEMBER = [
    "name",
    "profession",
    "student",
    "researcher",
    "interest",
    "working on",
    "studying",
    "favourite",
    "from",
    "live"
]


def should_save_fact(user_message):
    msg = user_message.lower()

    return any(
        keyword in msg
        for keyword in FACTS_TO_REMEMBER
    )


def extract_fact(user_message):
    return user_message.strip()


def build_prompt(user_message):

    rag_chunks = retrieve(
        user_message,
        n_results=5
    )

    rag_context = ""

    if rag_chunks:

        rag_context = """
IMPORTANT:

The following retrieved passages come from Stephen Hawking's books,
interviews, lectures, and related materials.

If the answer exists in these passages,
you MUST use them as your primary source of information.

Do not ignore retrieved material.

Do not claim you do not remember something if the retrieved
context contains the answer.

Retrieved Context:
"""

        for chunk in rag_chunks:

            rag_context += (
                f"\n[Source: {chunk['source']}]\n"
                f"{chunk['text']}\n"
            )

    long_term_context = long_term.format_for_prompt()

    short_term_context = short_term.format_for_prompt()

    prompt = f"""
{HAWKING_SYSTEM_PROMPT}

{long_term_context}

{rag_context}

Conversation so far:

{short_term_context}

User Question:
{user_message}

Instructions:

1. Remain in character as Stephen Hawking.
2. Use retrieved context whenever relevant.
3. Prefer retrieved information over general model knowledge.
4. If retrieved context contains the answer, use it.
5. Do not say you cannot remember something if it appears in the retrieved context.
6. Give clear and direct answers.

Stephen Hawking:
"""

    return prompt


def chat(user_message):

    if should_save_fact(user_message):
        long_term.add(
            extract_fact(user_message)
        )

    rag_chunks = retrieve(
        user_message,
        n_results=5
    )

    prompt = build_prompt(
        user_message
    )

    response = model.generate_content(
        prompt
    )

    reply = response.text.strip()

    short_term.add(
        "user",
        user_message
    )

    short_term.add(
        "assistant",
        reply
    )

    sources = []

    for chunk in rag_chunks:

        source = chunk["source"]

        if source not in sources:
            sources.append(source)

    return {
        "response": reply,
        "sources": sources
    }


def reset_short_term():
    short_term.clear()
