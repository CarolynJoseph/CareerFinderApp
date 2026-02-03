from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_modified_coverletter(description, sample_coverletter):
    description = "We need a professional software engineer skilled in Python and machine learning to join our dynamic team. The ideal candidate will have experience in developing scalable applications and a strong understanding of AI technologies."
    sample_coverletter= "i am a software engineer with experience in python and machine learning..."
    response = query({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Modify the <sample_coverletter> to better fit the <job_description>. Do not add fluff or unnecessary information. "
                    },
                    {
                        "type": "text",
                        "text": f"Job Description: {description.strip()}"
                    },
                    {
                        "type": "text",
                        "text": f"Sample Coverletter: {sample_coverletter.strip()}"
                    }
                ]
            }
        ],
        "model": "ServiceNow-AI/Apriel-1.6-15b-Thinker:together"
    })
    return response["choices"][0]["message"]["content"]

