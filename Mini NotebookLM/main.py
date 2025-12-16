# uv add gradio chromadb sentence-transformers transformers pdfplumber

import os
import shutil
import tempfile
import gradio as gr

from rag.reader import read_text, chunk_text
from rag.vectorstore import ChromaRAG
from llm.answerGenerator import AnswerGenerator

# Create RAG engine and generator once
rag = ChromaRAG()
gen = AnswerGenerator()

# -----------------------------
# 1. Upload : Extract Text → Chunk → Store → Ready for Questions
# -----------------------------
def upload_file(uploaded):
    if not uploaded:
        return "Please upload a file."

    # Gradio gives us the file path as a string
    src_path = str(uploaded)

    if not os.path.exists(src_path):
        return f"File not found: {src_path}"

    # Copy file to a safe temporary folder
    temp_dir = tempfile.mkdtemp()
    dest_path = os.path.join(temp_dir, os.path.basename(src_path))
    shutil.copy(src_path, dest_path)

    # 1. Extract Text
    text = read_text(dest_path)
    # 2. Extract Text
    chunks = chunk_text(text)

    # 3. Store in Vector DB
    rag.build(chunks)

    return f"Indexed {len(chunks)} chunks. You can now ask questions."


# -----------------------------
# 2. Answer a question
# -----------------------------
def ask_question(question):
    if rag.collection is None:
        return "Please upload and index a document first."

    # Retrieve top matching chunks
    docs = rag.search(question, top_k=4)

    # Extract only the text parts
    contexts = [d for d in docs]

    # Generate answer
    answer = gen.answer(question, contexts)

    # Show sources (shortened)
    src_list = "\n".join([f"- {d[:120]}..." for d in contexts])

    return answer + "\n\nSources:\n" + src_list


# -----------------------------
# 3. Build app UI - Gradio
# -----------------------------
with gr.Blocks(title="Mini NotebookLM App") as demo:
    gr.Markdown("# 📄 Mini NotebookLM (ChromaDB + FLAN-T5)")

    with gr.Row():
        with gr.Column():
            file_in = gr.File(label="Upload PDF or TXT")
            upload_btn = gr.Button("Index Document")
            status = gr.Textbox(label="Status")

        with gr.Column():
            question_in = gr.Textbox(label="Ask a Question")
            ask_btn = gr.Button("Ask")
            answer_out = gr.Textbox(label="Answer", lines=10)

    upload_btn.click(upload_file, inputs=file_in, outputs=status)
    ask_btn.click(ask_question, inputs=question_in, outputs=answer_out)


# Run app
if __name__ == "__main__":
    demo.launch()
