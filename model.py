from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

with open('faqs.json', 'r') as file:
    data = json.load(file)

faq_data = []
for section, qa_list in data.items():
    for qa in qa_list:
        faq_data.append({"question": qa["question"], "answer": qa["answer"]})

semantic_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

faq_questions = [faq['question'] for faq in faq_data]
question_embeddings = semantic_model.embed_documents(faq_questions)

def get_closest_answer(user_query):
    query_embedding = semantic_model.embed_query(user_query)

    similarities = cosine_similarity([query_embedding], question_embeddings)[0] 

    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
    threshold = 0.75

    if best_score >= threshold:
        return faq_data[best_idx]['answer'], faq_data[best_idx]['question']
    else:
        return None, None

def chatbot(user_query):
    closest_answer, closest_question = get_closest_answer(user_query)

    if closest_answer:
        return closest_answer
    else:
        return "Sorry, I couldn't find an appropriate answer. Do you want help with something else?"
