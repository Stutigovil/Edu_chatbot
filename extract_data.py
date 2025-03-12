
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection(name="courses")


url = "https://brainlox.com/courses/category/technical"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

try:
   
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()


    soup = BeautifulSoup(response.text, "html.parser")

    
    courses = soup.find_all("div", class_="courses-content")


    for idx, course in enumerate(courses):
        title = course.find("h3").text.strip() if course.find("h3") else "Title Not Found"
        price = course.find(class_="price-per-session").text.strip() if course.find(class_="price-per-session") else "$30"
        description = course.find("p").text.strip() if course.find("p") else "No Description"
        no_lesson = course.find("li").text.strip() if course.find("i") else "No Lesson Info"
        description_link= "https://brainlox.com/courses/category/technical"
      

        
        embedding = model.encode(title).tolist()

        # Store in vector database
        collection.add(
            ids=[str(idx)],
            embeddings=[embedding],
            metadatas=[{"title": title, "price": price, "description": description, "lessons": no_lesson ,"description_link":description_link}]
        )

    print("Embeddings stored successfully in ChromaDB!")

except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)