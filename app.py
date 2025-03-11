
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from sentence_transformers import SentenceTransformer
import chromadb
import re
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(12)
socketio = SocketIO(app)


model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection(name="courses")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    response = chat_logic(msg)
    emit("response", response)

def chat_logic(query):
    
    if query.lower() in ["hi", "hello", "hey"]:
        return "Hey there! How can I help you? 😊"
    
    if query.lower() in ["How are You"]:
        return "I am good! How can I help you? 😊"

    query_embedding = model.encode(query).tolist()
    search_results = collection.query(query_embeddings=[query_embedding], n_results=1)

    if not search_results["metadatas"][0]:
        return "I couldn't find anything related to that. Can you ask in another way?"

    course = search_results["metadatas"][0][0]
    title, price, description, lessons = course["title"], course["price"], course["description"], course["lessons"]

    
    if re.search(r"\bprice\b|\bcost\b|\bfee\b", query, re.IGNORECASE):
        return f" **{title}** costs {price}. \n"
    elif re.search(r"\blesson\b|\bmodule\b|\bhow many\b", query, re.IGNORECASE):
        return f" **{title}** has {lessons} lessons.\n"
    elif re.search(r"\bdescription\b|\bwhat is\b|\babout\b", query, re.IGNORECASE):
        return f" **{title}**: {description}\n"
    else:
        return f" **{title}**\n\n  Price: {price}\n\n  Description: {description}\n\n  Lessons: {lessons}\n\n "

if __name__ == "__main__":
    socketio.run(app, debug=True)
