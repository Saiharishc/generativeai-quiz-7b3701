import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/api/topics')
def get_topics():
    # In a real app, this would fetch topics from a database or configuration.
    # For now, we return a hardcoded list.
    return [
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision"
    ]

@app.get('/api/quizzes/topic/{topic_name}')
def get_quizzes_by_topic(topic_name: str):
    # Mock data for quizzes. Replace with actual data retrieval.
    mock_quizzes = {
        "Machine Learning": [
            {"id": 1, "question": "What is a key advantage of ensemble methods?", "topic": "Machine Learning"},
            {"id": 2, "question": "Which algorithm is commonly used for dimensionality reduction?", "topic": "Machine Learning"}
        ],
        "Deep Learning": [
            {"id": 3, "question": "What does CNN stand for?", "topic": "Deep Learning"},
            {"id": 4, "question": "Which activation function is popular in hidden layers of neural networks?", "topic": "Deep Learning"}
        ],
        "Natural Language Processing": [
            {"id": 5, "question": "What is tokenization in NLP?", "topic": "Natural Language Processing"},
            {"id": 6, "question": "What does RNN stand for?", "topic": "Natural Language Processing"}
        ],
        "Computer Vision": [
            {"id": 7, "question": "What is image segmentation?", "topic": "Computer Vision"},
            {"id": 8, "question": "What is a common technique for object detection?", "topic": "Computer Vision"}
        ]
    }
    return mock_quizzes.get(topic_name, [])

@app.get('/api/quizzes/search/{query}')
def search_quizzes(query: str):
    # Mock data for search. Replace with actual data retrieval.
    all_quizzes = [
        {"id": 1, "question": "What is a key advantage of ensemble methods?", "topic": "Machine Learning"},
        {"id": 2, "question": "Which algorithm is commonly used for dimensionality reduction?", "topic": "Machine Learning"},
        {"id": 3, "question": "What does CNN stand for?", "topic": "Deep Learning"},
        {"id": 4, "question": "Which activation function is popular in hidden layers of neural networks?", "topic": "Deep Learning"},
        {"id": 5, "question": "What is tokenization in NLP?", "topic": "Natural Language Processing"},
        {"id": 6, "question": "What does RNN stand for?", "topic": "Natural Language Processing"},
        {"id": 7, "question": "What is image segmentation?", "topic": "Computer Vision"},
        {"id": 8, "question": "What is a common technique for object detection?", "topic": "Computer Vision"}
    ]
    query_lower = query.lower()
    return [quiz for quiz in all_quizzes if query_lower in quiz['question'].lower() or query_lower in quiz['topic'].lower()]

@app.get('/api/quiz/{quiz_id}/answer')
def get_quiz_answer(quiz_id: int):
    # Mock data for answers. Replace with actual data retrieval.
    mock_answers = {
        1: {"explanation": "Ensemble methods combine multiple models to improve predictive performance and robustness, reducing variance and bias."},
        2: {"explanation": "Principal Component Analysis (PCA) is a widely used algorithm for dimensionality reduction."},
        3: {"explanation": "CNN stands for Convolutional Neural Network, a class of deep neural networks, most commonly applied to analyzing visual imagery."},
        4: {"explanation": "The Rectified Linear Unit (ReLU) is a popular activation function for hidden layers due to its simplicity and effectiveness."},
        5: {"explanation": "Tokenization is the process of breaking down a sequence of text into smaller units called tokens, which can be words, subwords, or characters."},
        6: {"explanation": "RNN stands for Recurrent Neural Network, designed to process sequential data like text or time series."},
        7: {"explanation": "Image segmentation is the process of partitioning a digital image into multiple segments (sets of pixels, also known as image objects)."},
        8: {"explanation": "Region-based Convolutional Neural Networks (R-CNN) and YOLO (You Only Look Once) are common techniques for object detection."}
    }
    return mock_answers.get(quiz_id, {"explanation": "Answer not found."})

# Serve frontend static files and handle routing
if os.path.isdir("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

    @app.get("{*path}")
    def serve_frontend_index(path: str):
        # This route handles all GET requests not matching API routes
        # and serves the frontend index.html.
        # The frontend router will handle the actual path resolution.
        return FileResponse("frontend/build/index.html")
else:
    @app.get("/api/health")
    def health_check():
        return {"status": "API is running, frontend build not found."}



