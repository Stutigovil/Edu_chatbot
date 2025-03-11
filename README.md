# AI Chatbot with Course Search

This is a chatbot web application that interacts with users and provides information about technical courses. It integrates a web scraper, vector-based search, and a real-time chat interface.

## Features
- **Real-time Chat:** Uses Flask-SocketIO for real-time communication.
- **Vector Search:** Implements ChromaDB and SentenceTransformer for semantic search.
- **Web Scraping:** Fetches course details dynamically from `brainlox.com`.

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Setup Instructions

1. **Clone the Repository**
   ```sh
   git clone <https://github.com/Stutigovil/Edu_chatbot.git>

2. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
3. **Run the Scrapper**
    ```sh
    python extract_data.py
4. **Start the server**
    ```sh
    python app.py

**Project structure**
├── app.py              
├── extract_data.py     
├── templates/
│   ├── index.html      
├── vector_db/
├── requirements.txt
└── README.md 

**Technology Used**

Flask - Web framework
Flask-SocketIO - Real-time WebSockets for chat
BeautifulSoup4 - Web scraping
ChromaDB - Vector database for semantic search
SentenceTransformers - AI model for text embeddings
