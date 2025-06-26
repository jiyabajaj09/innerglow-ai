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

        # Give an explicit style example in the prompt
        prompt = (
            "You are a warm, supportive self-help coach who writes short, natural-sounding, encouraging messages. "
            "Your task is to take a negative thought and reframe it into a kind, hopeful, and uplifting message that acknowledges the struggle and emphasizes growth. "
            "Do not repeat the negative thought. Offer empathy and make the person feel heard. "
            "Sound like a caring friend or mentor. "
            "Your message should feel authentic, positive, and motivational — like a personal pep talk. "
            "Avoid sounding robotic. Aim for 1-2 friendly sentences that inspire confidence and persistence. "
            "Here is an example:\n\n"
            "Negative thought: 'I will never improve at coding.'\n"
            "Positive reframe: 'You're still learning, and every bit of practice is progress. Keep going — your skills will grow with patience and persistence!'\n\n"
            f"Now reframe this thought in a similar style:\nNegative thought: '{thought}'\nPositive reframe:"
        )


        # Generate a positive reframe
        reframed = reframe_model(
            prompt,
            num_return_sequences=1,
            truncation=True,
        )[0]['generated_text']

        return {"reframed_thought": reframed.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
