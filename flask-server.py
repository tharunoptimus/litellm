# Load the required libraries
# from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# The base model that is to be fine-tuned with alpaca dataset
base_model_name = "currentlyexhausted/lite-llm"

# Load the pre-trained flan T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained(base_model_name)
tokenizer = T5Tokenizer.from_pretrained(base_model_name)

# Move the model to the GPU
# Checking if GPU is available and setting device type
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device.type, "is available")
print(torch.get_num_threads(), "threads available!")

# Import the necessary libraries
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# Define a GET endpoint
@app.route("/")
def index():
    return send_file("./index.html")

@app.route("/generate", methods=['GET'])
def litellm():
  input_text = request.args.get('prompt')
  input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

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

  # Convert the output token ids to text
  return tokenizer.decode(output[0], skip_special_tokens=True)

# Run the app
if __name__ == "__main__":
    app.run()
