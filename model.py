from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json

with open('faqs.json', 'r') as file:
    data = json.load(file)

faq_data = []

for section, qa_list in data.items():
    for qa in qa_list:
        faq_data.append({"question": qa["question"], "answer": qa["answer"]})

semantic_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

faq_questions = [faq['question'] for faq in faq_data]

if semantic_model:
    question_embeddings = FAISS.from_texts(faq_questions, semantic_model)

def get_closest_answer(user_query):
    docs_with_scores = question_embeddings.similarity_search_with_score(user_query, k=1)
    
    question = None
    threshold = 1.5
    best_match, score = docs_with_scores[0]
    content = best_match.page_content
    
    if score <= threshold:
        question = content

    if question is not None:
        
        closest_match_idx = faq_questions.index(question)
        
        return faq_data[closest_match_idx]['answer'], faq_data[closest_match_idx]['question']
    else:
        return None, None

def chatbot(user_query):
    closest_answer, closest_question = get_closest_answer(user_query)
    
    if closest_answer:
        return closest_answer
    else:
        return "Sorry, I couldn't find an appropriate answer. Do you want help with something else?"
