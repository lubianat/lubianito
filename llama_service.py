# llama_service.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LlamaService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("andrijdavid/Llama-3-2B-Base")
        self.model = AutoModelForCausalLM.from_pretrained("andrijdavid/Llama-3-2B-Base")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
    
    def interpret_contest(self, description):
        prompt = f"Here is a contest description: {description}. Is it open for Brazilian photographers?"
        output = self.generator(prompt, max_length=100, num_return_sequences=1)
        return output[0]['generated_text']
