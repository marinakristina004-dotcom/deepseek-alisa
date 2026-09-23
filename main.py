import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_text}],
            },
            timeout=10
        )
        # Выводим весь ответ DeepSeek в лог Render
        print("DEEPSEEK RESPONSE:", response.status_code, response.text, flush=True)
        
        data = response.json()
        
        # Если в ответе есть ошибка — сообщаем о ней
        if "error" in data:
            error_msg = data["error"].get("message", "Неизвестная ошибка DeepSeek")
            print("DEEPSEEK ERROR:", error_msg, flush=True)
            answer = f"Ошибка DeepSeek: {error_msg}"
        else:
            answer = data["choices"][0]["message"]["content"]
            
    except Exception as e:
        print("EXCEPTION:", str(e), flush=True)
        answer = "Извините, произошла ошибка. Попробуйте позже."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
