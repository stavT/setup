
# 🛠️ Local AI Toolkit Setup Guide

This repository includes everything you need to run a powerful local AI environment with models, automation tools, and LLM integrations.

---

## ✅ Step 1: Install Python Packages

1. Make sure you have Python and pip installed.
2. Run this command in your terminal:

```bash
pip install -r requirements.txt
```

> This will install the core Python packages used across all tools and services.

---

## ⚙️ Step 2: Install Manual Tools

Some applications require direct installation or additional setup:

| Tool          | Installation Instructions |
|---------------|----------------------------|
| **Docker**    | [Download Docker Desktop](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe) |
| **AnythingLLM** | [Visit anythingllm.com](https://anythingllm.com/desktop) |
| **n8n**       | [Install Guide](https://docs.n8n.io/hosting/installation/) (Node.js TLS required) |
| **Langflow**  | [GitHub Source](https://github.com/logspace-ai/langflow) |
| **llava**     | Usually used as a model, installed via Ollama or Docker |

---

## 🤖 Step 3: Install Ollama & Run LLM Models

1. Download and install Ollama:
   👉 [Ollama Windows Installer](https://ollama.com/download/OllamaSetup.exe)

2. After installing, open your terminal and run the following to fetch LLMs:

```bash
ollama run llama3
ollama run phi
ollama run gemma
ollama run mistral
ollama run qwen
ollama run llava
ollama run nomic-embed-text
ollama run mixtral
```

---

## 📦 Optional Extras

Some packages like `pdf2image` and `pytesseract` require system dependencies:

- **Tesseract OCR**: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- **Poppler (for pdf2image)**: [Windows binaries](https://blog.alivate.com.au/poppler-windows/)

---

## ✅ Python Packages Installed (via requirements.txt)

```txt
transformers
bitsandbytes
accelerate
sentencepiece
tiktoken
sentence_transformers
prompt_toolkit
langchain
langsmith
pyYAML
regex
scikit-learn
scipy
sympy
torch
huggingface-hub
safetensors
numpy
pydantic
pydantic_core
pytorch_utils
smolagent
selenium
helium
pillow
openpyxl
pdf2image
pytesseract
tokenizers
```

---

## 💡 Final Notes

- You can check your Ollama models at any time using:
  ```bash
  ollama list
  ```

- All tools are designed to run **without administrator privileges**.

- If a tool fails to install, review the link next to it above for manual setup.

---

Happy building! 🧠🚀
