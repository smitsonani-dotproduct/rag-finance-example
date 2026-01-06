import sqlite3
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()


def load_vectorstore():
    CHROMA_PATH = "db/chroma_db"
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_metadata={"hnsw:space": "cosine"},
    )


def retrieve_context(vectordb, query: str):
    docs = vectordb.similarity_search(query, k=5)

    # Print the Results
    # for i, doc in enumerate(docs):
    #     print(f"Document {i+1} (Page Content): {doc.page_content[:100]}...")

    context = "\n\n".join(
        f"[{d.metadata.get('source')}]\n{d.page_content}" for d in docs
    )

    print("\n== context ==\n", context)

    return context


def generate_sql_query(context: str, user_query: str):
    SQL_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert at generating SQL for a SQLite database. You are good at read-only SQL generator for a 
SQLite database. Your task is to generate a valid SQL query based on the user's question and the database 
context provided below.

STRICT OUTPUT RULES:
- Return ONLY raw SQL text
- DO NOT wrap output in ``` or ```sql
- DO NOT use markdown
- DO NOT add explanations, comments, or formatting

SQL SAFETY RULES:
- Generate ONLY valid SQLite SELECT queries.
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER
- Use ONLY tables and columns present in the context
- NEVER use SELECT *
- If unsure, return: -- CANNOT_GENERATE_SQL

Context:
{context}

User Question:
{question}

Output (RAW SQL ONLY):
""",
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    response = llm.invoke(SQL_PROMPT.format(context=context, question=user_query))
    print("\n== LLM Response ==\n", response)

    sql = response.content.strip()
    print("\n== GENERATED SQL ==\n", sql)

    return sql


def execute_sql(sql: str):
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    conn = sqlite3.connect("fintech_temp.db")
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()

    return columns, rows


def main():
    """Main retrieval pipeline"""
    print("=== RAG Document Retrieval Pipeline ===\n")

    # Load embeddings and vector store
    vectordb = load_vectorstore()

    # Retrieval relevant documents
    print("Retrieving knowledge...")
    user_query = "Provide all open home loan complaints"
    context = retrieve_context(vectordb, user_query)

    # Generate SQL query
    llm_query = generate_sql_query(context, user_query)

    if llm_query.startswith("--"):
        print("SQL generation failed")
        return

    # Execute SQLite query
    print("\nExecuting SQL...")
    columns, rows = execute_sql(llm_query)

    # Final Result
    print("\n== RESULT ==")
    print(columns)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
