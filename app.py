
import streamlit as st
from agent import chat, reset_short_term, long_term

HAWKING_AVATAR = "assets/hawking.jpg"

st.set_page_config(
    page_title="Stephen Hawking Digital Twin",
    layout="wide"
)

col1, col2 = st.columns([1, 8])

with col1:
    st.image(HAWKING_AVATAR, width=90)

with col2:
    st.title("Stephen Hawking Digital Twin")

st.caption(
    "A simulation of Stephen Hawking powered by RAG, memory, and Gemini 2.5 Flash"
)

with st.sidebar:

    st.header("Memory Dashboard")
    st.subheader("Long Term Memory")

    memories = long_term.get_all()

    if memories:
        for m in memories:
            st.markdown(
                f"- {m['fact']} *(saved: {m['timestamp']})*"
            )
    else:
        st.info("Nothing remembered yet.")

    st.divider()

    if st.button("Clear Conversation"):
        reset_short_term()
        st.session_state.messages = []
        st.rerun()

    if st.button("Clear Long Term Memory"):
        long_term.clear()
        st.rerun()

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "I am Stephen Hawking. Or rather, a simulation of me. "
                "I find the concept philosophically amusing. "
                "Ask me anything about black holes, the origin of the universe, "
                "or the nature of time."
            ),
            "sources": []
        }
    ]

for msg in st.session_state.messages:

    avatar = None

    if msg["role"] == "assistant":
        avatar = HAWKING_AVATAR

    with st.chat_message(msg["role"], avatar=avatar):

        st.markdown(msg["content"])

        if (
            msg["role"] == "assistant"
            and "sources" in msg
            and msg["sources"]
        ):
            st.caption(
                "Sources Used: " +
                ", ".join(msg["sources"])
            )

if prompt := st.chat_input("Ask Hawking anything..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message(
        "assistant",
        avatar=HAWKING_AVATAR
    ):

        with st.spinner("Hawking is thinking..."):
            result = chat(prompt)

        response = result["response"]
        sources = result["sources"]

        st.markdown(response)

        if sources:
            st.caption(
                "Sources Used: " +
                ", ".join(sources)
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "sources": sources
        }
    )

