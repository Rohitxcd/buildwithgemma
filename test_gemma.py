import kagglehub
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print("Downloading model...")

MODEL_PATH = kagglehub.model_download(
    "google/gemma-4/transformers/gemma-4-12b"
)

print("Model downloaded to:", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

prompt = "What is Artificial Intelligence?"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(
    **inputs,
    max_new_tokens=50
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))