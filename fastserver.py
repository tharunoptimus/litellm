# Load the required libraries
# from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import os

# The base model that is to be fine-tuned with alpaca dataset
base_model_name = "currentlyexhausted/lite-llm"

# Load the pre-trained flan T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained(base_model_name)
tokenizer = T5Tokenizer.from_pretrained(base_model_name)

# Move the model to the GPU
# Checking if GPU is available and setting device type
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device.type, "is available")
torch.set_num_threads(1) # Setting torch to use a single thread 
print(torch.get_num_threads(), "threads available!")

# Import the necessary libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_methods=["GET"],  # Specify the allowed HTTP methods
    allow_headers=["*"],  # Allow all headers in the requests
)

def lite_llm(prompt: str) -> str:
    # Your logic to generate the response string based on the prompt
    response = f"Response to '{prompt}'"
    return response

@app.get("/generate")
def endpoint(prompt: str):
    response = litellm(prompt)
    return {"response": response}


def litellm(prompt):
  input_text = prompt
  input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

  # Generate the output with modified settings
  output = model.generate(
      input_ids=input_ids,
      max_length=512,  # Increase max_length
      num_beams=8,  # Increase num_beams
      no_repeat_ngram_size=4,  # Increase no_repeat_ngram_size
      early_stopping=True,
      top_p=0.95, # Sample from the top 95% of the distribution
      temperature=0.5 # Control the level of randomness
  )

  # Convert the output token ids to text
  return tokenizer.decode(output[0], skip_special_tokens=True)

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
