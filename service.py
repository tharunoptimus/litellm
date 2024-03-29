print("Importing Necessary Libraries")
# Load the required libraries
from transformers import T5Tokenizer, T5ForConditionalGeneration, TextStreamer, TextIteratorStreamer
from threading import Thread
import torch
import time
import os

# The base model that is to be fine-tuned with alpaca dataset
base_model_name = "currentlyexhausted/lite-llm"

print("Loading the required model...")
# Load the pre-trained flan T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained(base_model_name)
tokenizer = T5Tokenizer.from_pretrained(base_model_name)

# Move the model to the GPU
# Checking if GPU is available and setting device type
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device.type, "is available")
torch.set_num_threads(1) # Setting torch to use a single thread 
print("Running on", torch.get_num_threads(), "threads\n")

def litellm(prompt):
    input_text = prompt
    
    print("Encoding the prompt into tokens...\n")
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

    print("Model is now generating the response...\n\n")
    start = time.process_time()
    # Generate the output with modified settings
    output = model.generate(
      input_ids=input_ids,
      max_length=512,  # Increase max_length
      num_beams=1,  # Increase num_beams
      no_repeat_ngram_size=4,  # Increase no_repeat_ngram_size
      early_stopping=True,
      top_p=0.95, # Sample from the top 95% of the distribution
      temperature=0.5 # Control the level of randomness
    )
    print("Took: ", time.process_time() - start)
    
    # Convert the output token ids to text
    return tokenizer.decode(output[0], skip_special_tokens=True)


async def stream_litellm(prompt, websocket):
    input_text = prompt
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

    generation_kwargs = dict(
        input_ids=input_ids,
        max_length=512,  # Increase max_length
        num_beams=1,  # Increase num_beams
        no_repeat_ngram_size=4,  # Increase no_repeat_ngram_size
        early_stopping=True,
        top_k=50,
        streamer=streamer,
        top_p=0.95, # Sample from the top 95% of the distribution
        temperature=0.3 # Control the level of randomness
    )

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    async for new_text in streamer:
        print(new_text, end="")
        await websocket.send_text(new_text)


# Import the necessary libraries for the API
from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_methods=["GET"],  # Specify the allowed HTTP methods
    allow_headers=["*"],  # Allow all headers in the requests
)

@app.get("/")
def root():
    return FileResponse("./index.html")

@app.get("/generate")
def endpoint(prompt: str):
    response = litellm(prompt)
    return {"response": response}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            prompt = data
            await stream_litellm(prompt, websocket)
    except Exception as e:
        await websocket.close()
        print(e)


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 

