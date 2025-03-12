
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
    
    if query.lower() in ["how are you"]:
        return "I am good! How can I help you? 😊"

    query_embedding = model.encode(query).tolist()
    search_results = collection.query(query_embeddings=[query_embedding], n_results=2)

    if not search_results["metadatas"][0]:
        return "I couldn't find anything related to that. Can you ask in another way?"

    course = search_results["metadatas"][0][0]
    title, price, description, lessons, description_link = course["title"], course["price"], course["description"], course["lessons"] , course["description_link"]

    
    if re.search(r"\bprice\b|\bcost\b|\bfee\b", query, re.IGNORECASE):
        return f"  costs {price}. \n"
    elif re.search(r"\blesson\b|\bmodule\b|\bhow many\b", query, re.IGNORECASE):
        return f"{lessons}.\n"
    elif re.search(r"\bdescription\b|\bwhat is\b|\babout\b", query, re.IGNORECASE):
        return f" {description}\n"
    elif re.search(r"\bFurther description\b|\bmore details\b|\bmore about\b", query, re.IGNORECASE):
        return f" {description_link}\n"
    else:
        return f" **{title}**\n\n  Price: {price}\n\n  Lessons: {lessons}\n\n   Description: {description}\n\n  For further detail:{description_link}\n\n"

if __name__ == "__main__":
    socketio.run(app, debug=True)
