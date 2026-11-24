
import streamlit as st

from openai import (
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    APIError
)

from config import API_KEY

from rag import (
    create_retriever,
    retrieve_context
)

from llm import (
    generate_answer,
    rewrite_question,
    classify_ticket
)

from agent import (
    build_agent,
    run_agent
)


# Page configuration
st.set_page_config(
    page_title="ProcureAI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ProcureAI")

st.caption(
    "AI-powered Procurement Knowledge Assistant"
)

st.info(
    "Learning project using fictional company data."
)


# Validate configuration
if not API_KEY:
    st.warning("API configuration is missing.")
    st.stop()


# Cache the vector index
@st.cache_resource
def initialize_rag():
    return create_retriever()


# Sidebar
with st.sidebar:

    st.header("Application Modes")

    mode = st.selectbox(
        "Choose mode",
        [
            "General AI",
            "Document Q&A",
            "AI Agent",
            "Ticket Classification"
        ]
    )

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("Technologies")

    st.write("""
    - Python
    - Generative AI
    - LangChain
    - Hugging Face
    - FAISS
    - RAG
    - AI Agents
    - Streamlit
    """)


# Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_mode" not in st.session_state:
    st.session_state.previous_mode = mode


# Reset history when mode changes
if st.session_state.previous_mode != mode:

    st.session_state.messages = []

    st.session_state.previous_mode = mode


# Structured output mode
if mode == "Ticket Classification":

    st.subheader("Support Ticket Classification")

    ticket = st.text_area(
        "Enter a fictional support ticket",
        max_chars=2000
    )

    if st.button("Classify Ticket"):

        if not ticket.strip():
            st.warning("Please enter a ticket.")

        else:

            try:
                with st.spinner(
                    "Classifying ticket..."
                ):
                    result = classify_ticket(ticket)

                st.json(result)

            except Exception as error:
                st.error(
                    f"Classification failed: "
                    f"{type(error).__name__}"
                )


# Chat modes
else:

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message.get("sources"):

                with st.expander("Retrieved evidence"):

                    for source in message["sources"]:

                        st.write(
                            f"Chunk {source['id']}"
                        )

                        st.write(source["text"])


    # Get user question
    question = st.chat_input(
        "Ask your question...",
        max_chars=2000
    )

    if question:

        history = [
            {
                "role": message["role"],
                "content": message["content"]
            }
            for message in st.session_state.messages
        ]

        with st.chat_message("user"):
            st.write(question)

        sources = []

        with st.chat_message("assistant"):

            try:

                with st.spinner("Processing..."):

                    # GENERAL MODE
                    if mode == "General AI":

                        answer = generate_answer(
                            question,
                            history
                        )

                    # RAG MODE
                    elif mode == "Document Q&A":

                        retriever = initialize_rag()

                        search_query = rewrite_question(
                            question,
                            history
                        )

                        context, sources = (
                            retrieve_context(
                                retriever,
                                search_query
                            )
                        )

                        answer = generate_answer(
                            question,
                            history,
                            context=context
                        )

                    # AGENT MODE
                    else:

                        retriever = initialize_rag()

                        agent = build_agent(
                            retriever
                        )

                        answer = run_agent(
                            agent,
                            question,
                            history
                        )

                    if not answer:
                        raise RuntimeError(
                            "Empty response"
                        )

                st.write(answer)

                if sources:

                    with st.expander(
                        "Retrieved evidence"
                    ):

                        for source in sources:

                            st.write(
                                f"Chunk {source['id']}"
                            )

                            st.write(source["text"])

                # Store successful interaction
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

                st.session_state.messages = (
                    st.session_state.messages[-10:]
                )

            except AuthenticationError:
                st.error("Invalid API credentials.")

            except RateLimitError:
                st.error("API limit or quota exceeded.")

            except APITimeoutError:
                st.error("Request timed out.")

            except APIConnectionError:
                st.error("Check your connection.")

            except APIError:
                st.error("API request failed.")

            except Exception as error:
                st.error(
                    f"Application error: "
                    f"{type(error).__name__}"
                )
