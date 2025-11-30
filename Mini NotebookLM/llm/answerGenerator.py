from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class AnswerGenerator:
    def __init__(self):
        model_name = "google/flan-t5-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def answer(self, question, contexts):
        # Combine all retrieved text into one simple context block
        context_text = "\n".join(contexts)

        # Build a simple prompt
        prompt = f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer:"

        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)

        # Generate output
        outputs = self.model.generate(inputs["input_ids"], max_length=256)

        # Decode and return answer
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
