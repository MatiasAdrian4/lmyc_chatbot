# LMYC Chatbot

- Export Groq API Key

```bash
export GROQ_API_KEY="..."
```

- Run Server

```bash
python main.py
```

- Start a conversation

```bash
curl -X POST http://127.0.0.1:8000/messages/ -F prompt="Hola"
```
