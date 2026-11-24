
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import KNOWLEDGE_FILE


def create_retriever():

    # 1. Load document
    loader = TextLoader(
        str(KNOWLEDGE_FILE),
        encoding="utf-8"
    )

    documents = loader.load()

    # 2. Split document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Knowledge document is empty.")

    # 3. Add source identifiers
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index + 1

    # 4. Load embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=(
            "sentence-transformers/all-MiniLM-L6-v2"
        ),
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    # 5. Create vector store
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # 6. Return retriever
    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


def retrieve_context(retriever, question):

    # Search for relevant chunks
    documents = retriever.invoke(question)

    sources = []

    for doc in documents:
        sources.append({
            "id": doc.metadata["chunk_id"],
            "text": doc.page_content
        })

    context = "\n\n".join(
        f"[Chunk {source['id']}]\n{source['text']}"
        for source in sources
    )

    return context, sources
