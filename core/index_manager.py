import os
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    load_index_from_storage
)
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from utils.vector_store import build_chroma_vector_store
from utils.index_store import build_index_store, get_existing_indexes


mongo_index_id = os.getenv("MONGODB_INDEX_ID", "chats")

Settings.llm = Ollama(model="deepseek-r1:8b", request_time=360.0)
Settings.embed_model = OllamaEmbedding(model_name="snowflake-arctic-embed2")

vector_store, vector_store_exists = build_chroma_vector_store()
index_store = build_index_store()

storage_context = StorageContext.from_defaults(
    vector_store = vector_store,
    index_store=index_store
)


def initialize_index() -> BaseQueryEngine:
    """Initializes the index for querying.

    Loads an existing index from storage if available, otherwise builds a new index.

    Returns:
        BaseQueryEngine: The query engine for the index.

    """
    index = None

    existing_indexes = get_existing_indexes()
    if len(existing_indexes) > 0:
        print("Loading existing index...")
        index = load_index_from_storage(storage_context=storage_context, index_id=mongo_index_id)
    else:
        print("Creating index...")
        index = build_vector_index()

    query_engine = index.as_query_engine(similarity_top_k=5)

    return query_engine

def build_vector_index():
    """Builds a new vector index from documents in the specified directory.

    Loads documents from the './data' directory, creates a vector index from these documents,
    and sets the index ID to the value specified in the 'mongo_index_id' variable.

    Returns:
        VectorStoreIndex: The newly created vector index.
    """
    documents = SimpleDirectoryReader(input_dir="./data").load_data(show_progress=True)

    index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)

    index.set_index_id(mongo_index_id)

    return index
