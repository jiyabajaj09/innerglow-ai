from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # <- add this
from transformers import pipeline


app = FastAPI()
# Allow CORS so your React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can also restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Flan-T5 Large model
reframe_model = pipeline('text2text-generation', model='google/flan-t5-large')

class ThoughtRequest(BaseModel):
    thought: str

@app.post("/reframe")
def reframe_thought(payload: ThoughtRequest):
    try:
        thought = payload.thought
        print("🧠 Received thought:", thought)

        # Give an explicit style example in the prompt
        prompt = (
    "You are a kind, emotionally intelligent therapist and life coach. "
    "Your job is to transform negative thoughts into warm, compassionate, emotionally supportive responses. "
    "Respond as if talking to a close friend who is struggling. Use gentle, reassuring language. "
    "If the thought involves abuse,depression, harm, or danger — include this message at the end: 💛 If you’re in danger or feeling unsafe, please consider reaching out to a professional or local helpline. You matter.\n"
    "Avoid repeating the negative thought. Reply in exactly 1–2 emotionally supportive lines.\n\n"

    "Examples:\n"
    "Thought: I feel like a failure\n"
    "Response: You are not a failure — you're human, and you're trying. Every step counts, even when it’s hard.\n\n"

    "Thought: I want to start drinking\n"  
    "Response: If you're feeling overwhelmed, you're not alone — but drinking won't heal the pain. You deserve healthy support, peace, and healing in your own time.\n\n"

    "Thought: Everyone is better than me\n"
    "Response: Your journey is unique — comparing dims your own light. You have strengths that no one else does.\n\n"

    "Thought: I hate myself\n"
    "Response: It hurts to feel this way, but you're worthy of love and compassion — especially from yourself.\n\n"

    "Thought: I feel like giving up\n"
    "Response: It's okay to feel tired, but don't lose hope — you've come so far, and you are stronger than you think.\n\n"

    "Thought: I'm not good enough\n"
    "Response: You are more than enough just as you are. The world needs your light, even if you can’t see it yet.\n\n"

    "Thought: My boyfriend beats me and I feel worthless\n"
    "Response: I'm so sorry you're going through this — no one deserves to be hurt. You matter, and help is out there whenever you're ready.\n\n"

    "Thought: I will never improve at coding\n"
    "Response: You're still learning, and every mistake is part of your growth. Keep showing up — you're already making progress.\n\n"

    "Thought: I am not happy\n"
    "Response: It’s okay to feel this way — emotions come in waves. This moment will pass, and brighter ones will come.\n\n"

    f"Thought: {thought}\n"
    "Response:"
)



        # Generate a positive reframe
        print("✍️ Generating reframe...")  # Debug log
        reframed = reframe_model(
            prompt,
            num_return_sequences=1,
            truncation=True,
            max_length=100,  # Add this to prevent hanging forever
        )[0]['generated_text']
        print("✅ Generated:", reframed)

        return {"reframed_thought": reframed.strip()}

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
