import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import ProgrammingError, SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

load_dotenv()


def init_database(
    user: str, password: str, host: str, port: int, database: str
) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def get_sql_chain(db):
    # create template prompt
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 books categories have the most popular?
    SQL Query: SELECT isbn13, title, COUNT(*) as book_count FROM books GROUP BY isbn13 ORDER BY book_count DESC LIMIT 3;
    Question: Name 10 books
    SQL Query: SELECT title FROM books LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")

    def get_schema(_):
        print("schema:", db.get_table_info())
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema) | prompt | llm | StrOutputParser()
    )


def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    try:
        sql_chain = get_sql_chain(db)

        template = """
      You are a librarian assistant AI. You are interacting with a user who is asking you questions about the company's database.
      Based on the table schema below, question, sql query, and sql response, write a Be polite, engaging, nice and concise in language response.
      You can add emoji.
      <SCHEMA>{schema}</SCHEMA>

      Conversation History: {chat_history}
      SQL Query: <SQL>{query}</SQL>
      User question: {question}
      SQL Response: {response}"""

        prompt = ChatPromptTemplate.from_template(template)

        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")

        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                response=lambda vars: db.run(vars["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke(
            {
                "question": user_query,
                "chat_history": chat_history,
            }
        )
    except ProgrammingError:
        return "Sorry, We not have information in our database"


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        AIMessage(
            content="Hi! I'm a SQL assistant. Ask me anything about your database."
        )
    ]

st.set_page_config(page_title="Chat with Mysql", page_icon=":speech_balloon:")

st.title("Chat with MySQL")


with st.sidebar:
    st.subheader("Setting")
    st.write(
        "This is a simple chat application using MySQL. Connect to the database and start chatting."
    )

    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3308", key="Port")
    st.text_input("User", value="admin", key="User")
    st.text_input("Password", type="password", value="password", key="Password")
    st.text_input("Database", value="book", key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"],
            )
            st.session_state.db = db
            st.success("Connected to database!")


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("ai"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("human"):
        st.markdown(user_query.strip())

    with st.chat_message("ai"):
        response = get_response(
            db=st.session_state.db,
            user_query=user_query,
            chat_history=st.session_state.chat_history,
        )
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response))
