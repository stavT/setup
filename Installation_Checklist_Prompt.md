- **Ollama** (Framework)
  - Install: `Windows:
https://ollama.com/download/OllamaSetup.exe
(Linux:
curl -fsSL https://ollama.com/install.sh | sh
Script Source:
https://github.com/ollama/ollama/blob/main/scripts/install.sh)`

- **UI - Open WebUI** (Framework)
  - Install: `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`
  - Note: https://github.com/open-webui/open-webui

- **Docker** (Framework)
  - Install: `Windows:
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_location=module
Linux:
https://docs.docker.com/desktop/linux/install/`
  - Note: https://www.docker.com/

- **AnythingLLM** (Framework)
  - Install: `https://anythingllm.com/desktop`
  - Note: ברירת מחדל של התוכנה: שמירה לוקאלית

- **n8n** (Framework)
  - Install: `יש כמה אופציות:
התקנה בסיסית - https://docs.n8n.io/hosting/starter-kits/ai-starter-kit/
https://docs.n8n.io/hosting/installation/docker/
https://docs.n8n.io/hosting/installation/npm/`
  - Note: חשוב - יש להתקין את התלויות (node.js (TLS) וכו

- **Langflow** (Framework)
  - Install: `https://docs.langflow.org/get-started-installation`
  - Note: לדוגמה: uv pip install langflow

- **llama3.3** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **phi4** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **llama3.2** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **qwen2.5** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **llava** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **gemma3** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **llama3.2‑vision** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **mixtral** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **llava‑llama3** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **phi4** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **mistral** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **nomic-embed-text** (LLM)
  - Install: `התקנה על ידי פקודת ollama pull`
  - Note: לתרחישי שימוש סטנדרטיים

- **microsoft/Phi-3-mini-4k-instruct** (LLM)
  - Install: `from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
out = generator("Tell me about quantum mechanics.", max_new_tokens=100)
print(out[0]["generated_text"])`
  - Note: לתרחישי שימוש מותאמים

- **mistralai/Mistral-7B-Instruct-v0.2** (LLM)
  - Install: `מצ"ב הקוד למשיכת המודל הרלוונטי ושמירתו לוקאלית לשימוש חוזר, בלי חיבור לאינטרנט. שמירה בצורה כזאת לא מצריכה חיבור "החוצה" אלא מאפשרת שימוש באופן לוקאלי (הערה: הספריות גם רשומות בטבלה פה) 
# Install necessary libraries before running:
# pip install transformers accelerate bitsandbytes

from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. Define the Hugging Face model name
model_name =mistralai/Mistral-7B-Instruct-v0.2"  # Replace with your desired model

# 2. Download the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_auth_token=True  # Required if the model needs authentication
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_8bit=True,   # 8-bit quantization to save memory
    use_auth_token=True
)

# 3. Save the model and tokenizer locally
local_path = "./local_llama_model"
tokenizer.save_pretrained(local_path)
model.save_pretrained(local_path)

# 4. (Important) Future loads should use only local files (no Internet)
# Example for loading securely without internet access:
# tokenizer = AutoTokenizer.from_pretrained(local_path, local_files_only=True)
# model = AutoModelForCausalLM.from_pretrained(local_path, device_map="auto", load_in_8bit=True, local_files_only=True)`
  - Note: לתרחישי שימוש מותאמים

- **meta-llama/Llama-3.2-3B-Instruct** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **Qwen/Qwen2.5-7B-Instruct** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **google/gemma-3-1b-it** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **llama3.3** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **llava** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **llama3.2 vision** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **llava llama3** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **Mixtral 8×7B** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **nomic‑embed‑text** (LLM)
  - Install: `ראה למעלה קוד. להחליף בחלק 2 עם שם מודל מתאים`
  - Note: לתרחישי שימוש מותאמים

- **transformers** (ספריית פייתון)
  - Install: `pip install`

- **bitsandbytes** (חבילת פייתון)
  - Install: `pip install`

- **accelerate** (חבילת פייתון)
  - Install: `pip install`

- **sentencepiece** (חבילת פייתון)
  - Install: `pip install`

- **tiktoken** (חבילת פייתון)
  - Install: `pip install`

- **sentence_transformers** (חבילת פייתון)
  - Install: `pip install`

- **util** (חבילת פייתון)
  - Install: `pip install`

- **prompt_toolkit** (חבילת פייתון)
  - Install: `pip install`

- **langchain** (חבילת פייתון)
  - Install: `pip install`

- **langchain-core** (חבילת פייתון)
  - Install: `pip install`

- **langchain-text-splitters** (חבילת פייתון)
  - Install: `pip install`

- **tokenizers** (חבילת פייתון)
  - Install: `pip install`

- **langsmith** (חבילת פייתון)
  - Install: `pip install`

- **pyYAML** (חבילת פייתון)
  - Install: `pip install`

- **regex** (חבילת פייתון)
  - Install: `pip install`

- **scikit-learn** (חבילת פייתון)
  - Install: `pip install`

- **scipy** (חבילת פייתון)
  - Install: `pip install`

- **sympy** (חבילת פייתון)
  - Install: `pip install`

- **torch** (חבילת פייתון)
  - Install: `pip install`

- **huggingface-hub** (חבילת פייתון)
  - Install: `pip install`

- **safetensors** (חבילת פייתון)
  - Install: `pip install`

- **numpy** (חבילת פייתון)
  - Install: `pip install`

- **pydantic** (חבילת פייתון)
  - Install: `pip install`

- **pydantic_core** (חבילת פייתון)
  - Install: `pip install`

- **pytorch_utils** (חבילת פייתון)
  - Install: `pip install`

- **smolagent** (חבילת פייתון)
  - Install: `pip install`

- **selenium** (חבילת פייתון)
  - Install: `pip install`

- **helium** (חבילת פייתון)
  - Install: `pip install`

- **pillow** (חבילת פייתון)
  - Install: `pip install`

- **openpyxl** (חבילת פייתון)
  - Install: `pip install`

- **AutoModelForQuestionAnswering** (חבילת פייתון)
  - Install: `pip install`

- **pdf2image** (חבילת פייתון)
  - Install: `pip install`

- **pytesseract** (חבילת פייתון)
  - Install: `pip install`

- **numpy** (חבילת פייתון)
  - Install: `pip install`

- **os** (חבילת פייתון)
  - Install: `pip install`

- **traceback** (חבילת פייתון)
  - Install: `pip install`
