
import streamlit as st
from pathlib import Path
import re
from decimal import Decimal

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="ProcureAI",
    page_icon="🤖",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge.txt"

# -----------------------------------
# General AI Sample Responses
# -----------------------------------

SAMPLE_ANSWERS = {
    "What is artificial intelligence?":
        "Artificial intelligence enables computers "
        "to perform tasks that normally require "
        "human intelligence.",

    "What is procurement?":
        "Procurement is the process of purchasing "
        "goods and services for an organization.",

    "What is RAG?":
        "RAG stands for Retrieval-Augmented Generation. "
        "It retrieves relevant information from documents "
        "before generating an answer.",

    "What is an AI agent?":
        "An AI agent is a system that uses reasoning "
        "and tools to complete tasks.",

    "What is a purchase order?":
        "A purchase order is a formal document issued "
        "by a buyer to a supplier."
}

def general_answer(question):

    question = question.strip().lower().rstrip("?")

    for sample, answer in SAMPLE_ANSWERS.items():
        if question == sample.lower().rstrip("?"):
            return answer

    return (
        "This is an API-free demonstration. "
        "Please try one of the suggested questions. "
        "Live AI responses are available in the full version."
    )


# -----------------------------------
# Local Document Retrieval
# -----------------------------------

@st.cache_data
def load_knowledge():

    if not KNOWLEDGE_FILE.exists():
        return []

    content = KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )

    chunks = re.split(r"\n+|(?<=[.!?])\s+", content)

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]


STOP_WORDS = {
    "what", "is", "the", "a", "an", "are",
    "how", "many", "can", "i", "of", "to",
    "for", "in", "does", "do", "and", "who",
    "it", "my", "per", "company", "allowed"
}


def tokenize(text):

    words = re.findall(r"\b\w+\b", text.lower())

    return {
        word.rstrip("s")
        for word in words
        if word not in STOP_WORDS
    }


def search_documents(question):

    chunks = load_knowledge()
    question_words = tokenize(question)

    results = []

    for index, chunk in enumerate(chunks):

        chunk_words = tokenize(chunk)

        score = len(
            question_words.intersection(chunk_words)
        )

        if score > 0:
            results.append({
                "id": index + 1,
                "text": chunk,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:3]


# -----------------------------------
# Purchase Approval Tool
# -----------------------------------

def check_approval(amount):

    if amount > Decimal("50000"):
        return "Manager approval required"

    return "Manager approval not required"


# -----------------------------------
# Rule-Based Ticket Classification
# -----------------------------------

def classify_ticket(ticket):

    text = ticket.lower()

    urgent_words = [
        "urgent", "critical", "emergency",
        "immediately", "blocked"
    ]

    priority = "High" if any(
        word in text for word in urgent_words
    ) else "Medium"

    if any(word in text for word in [
        "invoice", "payment", "billing"
    ]):

        category = "Finance"
        action = "Forward the ticket to the finance team."

    elif any(word in text for word in [
        "supplier", "vendor", "delivery", "purchase"
    ]):

        category = "Procurement"
        action = "Forward the ticket to the procurement team."

    elif any(word in text for word in [
        "error", "software", "login", "system", "technical"
    ]):

        category = "IT Support"
        action = "Forward the ticket to the IT support team."

    elif any(word in text for word in [
        "leave", "employee", "attendance"
    ]):

        category = "Human Resources"
        action = "Forward the ticket to the HR department."

    else:

        category = "General"
        action = "Review the ticket manually."

    return {
        "category": category,
        "priority": priority,
        "summary": ticket[:150],
        "suggested_action": action
    }


# -----------------------------------
# Sidebar
# -----------------------------------

st.sidebar.title("🤖 ProcureAI")

st.sidebar.success("API-Free Demo Mode")

mode = st.sidebar.radio(
    "Select Application Mode",
    [
        "General AI",
        "Document Q&A",
        "AI Agent Tools",
        "Ticket Classification",
        "About Project"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Demo Technology")

st.sidebar.markdown("""
- Python
- Streamlit
- Keyword Retrieval
- Rule-Based Classification
- Local Python Functions
""")

if st.sidebar.button("Clear Conversation"):

    st.session_state.messages = []

# -----------------------------------
# Main Header
# -----------------------------------

st.title("🤖 ProcureAI")

st.subheader(
    "Intelligent Procurement Knowledge Assistant"
)

st.info(
    "You are using the API-free portfolio demo. "
    "Live LLM responses, semantic RAG and autonomous "
    "agent reasoning are available in the original version."
)

col1, col2, col3 = st.columns(3)

col1.metric("Demo Features", "4")
col2.metric("LLM API Calls", "0")
col3.metric("LLM API Cost", "₹0")

st.divider()

# -----------------------------------
# General AI Mode
# -----------------------------------

if mode == "General AI":

    st.header("💬 General AI Demonstration")

    st.caption(
        "Answers are predefined examples, "
        "not live AI-generated responses."
    )

    with st.expander("Suggested Questions"):

        for question in SAMPLE_ANSWERS:
            st.write(question)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask a sample question...",
        max_chars=500
    )

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        answer = general_answer(question)

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.session_state.messages = (
            st.session_state.messages[-20:]
        )


# -----------------------------------
# Document Q&A Mode
# -----------------------------------

elif mode == "Document Q&A":

    st.header("📚 Document Q&A")

    st.caption(
        "This demo retrieves document text using keyword "
        "matching rather than semantic embeddings."
    )

    with st.expander("Suggested Questions"):

        st.write("How many casual leaves are allowed?")
        st.write("What is the purchase approval policy?")
        st.write("When should invoices be submitted?")
        st.write("What is the supplier registration process?")

    question = st.text_input(
        "Ask a question about company policies",
        max_chars=500
    )

    if st.button("Search Documents"):

        if not question.strip():

            st.warning("Please enter a question.")

        elif not KNOWLEDGE_FILE.exists():

            st.error("knowledge.txt file was not found.")

        else:

            results = search_documents(question)

            if results:

                st.subheader("Matching Document Evidence")

                st.write(results[0]["text"])

                with st.expander("Retrieved Sources"):

                    for result in results:

                        st.markdown(
                            f"**Source {result['id']}**"
                        )

                        st.write(result["text"])

                        st.caption(
                            f"Keyword matches: {result['score']}"
                        )

            else:

                st.warning(
                    "I could not find matching information "
                    "in the knowledge document."
                )

    with st.expander("View Company Knowledge Base"):

        for chunk in load_knowledge():
            st.write(chunk)


# -----------------------------------
# AI Agent Tools Mode
# -----------------------------------

elif mode == "AI Agent Tools":

    st.header("🛠️ AI Agent Tool Demonstration")

    st.caption(
        "These tools execute directly using Python. "
        "No autonomous LLM agent is running."
    )

    price = st.number_input(
        "Price per item (₹)",
        min_value=0.0,
        max_value=100000000.0,
        value=40000.0,
        step=100.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=10000,
        value=20,
        step=1
    )

    if st.button("Calculate Purchase"):

        total = Decimal(str(price)) * quantity

        approval = check_approval(total)

        st.success(
            f"Total purchase cost: ₹{total:,.2f}"
        )

        st.info(approval)

        st.subheader("Structured Tool Output")

        st.json({
            "price_per_item": price,
            "quantity": quantity,
            "total_amount": float(total),
            "approval_status": approval
        })

        with st.expander("Execution Workflow"):

            st.code(
                "User Input\n"
                "    ↓\n"
                "Calculate Purchase Total\n"
                "    ↓\n"
                "Check Approval Policy\n"
                "    ↓\n"
                "Return Result",
                language="text"
            )


# -----------------------------------
# Ticket Classification Mode
# -----------------------------------

elif mode == "Ticket Classification":

    st.header("🎫 Support Ticket Classification")

    st.caption(
        "This demonstration classifies tickets "
        "using predefined Python rules."
    )

    ticket = st.text_area(
        "Enter a support ticket",
        placeholder="The supplier submitted an incorrect invoice.",
        max_chars=1000
    )

    st.caption(
        "Use fictional examples only. "
        "Do not enter confidential company information."
    )

    if st.button("Classify Ticket"):

        if not ticket.strip():

            st.warning("Please enter a ticket.")

        else:

            result = classify_ticket(ticket)

            col1, col2 = st.columns(2)

            col1.metric(
                "Category",
                result["category"]
            )

            col2.metric(
                "Priority",
                result["priority"]
            )

            st.subheader("Structured JSON Output")

            st.json(result)

            st.success(result["suggested_action"])


# -----------------------------------
# About Project
# -----------------------------------

elif mode == "About Project":

    st.header("🚀 About ProcureAI")

    st.write("""
    ProcureAI is an independent portfolio project
    designed to demonstrate AI applications in
    procurement and enterprise operations.
    """)

    st.subheader("Original AI Application")

    st.markdown("""
    - Python
    - LLM API Integration
    - LangChain
    - Retrieval-Augmented Generation
    - FAISS Vector Database
    - Hugging Face Embeddings
    - AI Agents and Tool Calling
    - Pydantic Structured Outputs
    - Streamlit
    - Docker
    - Git and GitHub
    """)

    st.subheader("Public Demo Architecture")

    st.code(
        "User Interface\n"
        "      ↓\n"
        "Mode Selection\n"
        "      ↓\n"
        "Local Python Logic\n"
        "      ↓\n"
        "Document Search / Tools / Rules\n"
        "      ↓\n"
        "Display Result",
        language="text"
    )

    st.warning(
        "The public demo does not use a live LLM. "
        "It demonstrates the user interface and "
        "selected workflows of the original project."
    )

# -----------------------------------
# Footer
# -----------------------------------

st.divider()

st.caption(
    "ProcureAI | Independent Educational Project | "
    "Fictional Company Policies | API-Free Demo"
)
