import gradio as gr
from google import genai
from google.genai import types
import os

# ================= GEMINI CLIENT =================
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ================= DATA =================
subjects = [
    "General",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Computer Science",
    "Artificial Intelligence"
]

personalities = {
    "Friendly 😊": "You are friendly, motivating and explain simply.",
    "Academic 🎓": "You are formal, academic and structured.",
    "High School 👩‍🏫": "Explain slowly for 10th–12th students.",
    "Strict 😈": "Be strict, exam-oriented and challenging.",
    "LKG 🍼": "Explain like teaching a very small child using very simple words."
}

languages = {
    "English": "Respond in English.",
    "Kannada": "Respond fully in Kannada.",
    "Hindi": "Respond fully in Hindi.",
    "Telugu": "Respond fully in Telugu.",
    "Marathi": "Respond fully in Marathi."
}

# ================= STUDY CHAT FUNCTION =================
def ask_ai(question, subject, persona, language, mode):
    prompt = f"""
{personalities[persona]}
{languages[language]}

Subject: {subject}
Mode: {mode}

Explain clearly and helpfully.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            temperature=0.4,
            max_output_tokens=2000
        ),
        contents=question
    )
    return response.text

# ================= QUIZ FUNCTION =================
def generate_quiz(topic, subject, difficulty, language):
    difficulty_map = {
        "LKG 🍼": "Very very simple questions for kids.",
        "Easy 🙂": "Beginner friendly easy MCQs.",
        "Normal 📘": "Standard school-level MCQs.",
        "Strict 😈": "Exam-oriented tricky MCQs."
    }

    prompt = f"""
You are a quiz generator.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty_map[difficulty]}
Language rule: {languages[language]}

Generate exactly 5 MCQ questions.
Each question must have:
A) option
B) option
C) option
D) option

After each question clearly write:
Correct Answer: <option letter>
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            temperature=0.5,
            max_output_tokens=1500
        ),
        contents=prompt
    )

    return response.text

# ================= CSS =================
css = """
body {
    background: linear-gradient(135deg,#667eea,#764ba2);
}
.gradio-container {
    font-family: Poppins, sans-serif;
}
h1, h2, label {
    color: white;
}
.card {
    background: rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 16px;
}
textarea {
    border-radius: 14px !important;
    font-size: 16px;
}
button {
    background: linear-gradient(135deg,#ff9a9e,#fad0c4) !important;
    border-radius: 14px !important;
    font-weight: bold;
}
"""

# ================= UI =================
with gr.Blocks(css=css) as demo:

    gr.Markdown("<h1 align='center'>🌈 Personal AI Study Assistant</h1>")
    gr.Markdown("<p align='center' style='color:white'>Ask • Practice • Learn ✨</p>")

    with gr.Tabs():

        # ============ STUDY CHAT TAB ============
        with gr.Tab("🧠 Study Chat"):
            with gr.Column(elem_classes="card"):
                question = gr.Textbox(
                    label="✍️ Ask Your Question",
                    placeholder="Type your question here...",
                    lines=6
                )

                with gr.Row():
                    subject = gr.Dropdown(subjects, value="General", label="📚 Subject")
                    persona = gr.Dropdown(
                        list(personalities.keys()),
                        value="Friendly 😊",
                        label="🎭 Personality"
                    )

                with gr.Row():
                    language = gr.Dropdown(
                        list(languages.keys()),
                        value="English",
                        label="🌍 Language"
                    )
                    mode = gr.Radio(
                        ["General", "12th Syllabus"],
                        value="General",
                        label="📘 Mode"
                    )

                ask_btn = gr.Button("✨ Ask AI ✨")

            with gr.Column(elem_classes="card"):
                answer = gr.Textbox(label="🤖 Assistant Response", lines=10)

            ask_btn.click(
                ask_ai,
                inputs=[question, subject, persona, language, mode],
                outputs=answer
            )

        # ============ QUIZ TAB ============
        with gr.Tab("📝 Quiz & MCQs"):
            with gr.Column(elem_classes="card"):

                gr.Markdown("### 🧪 Practice MCQs")

                quiz_topic = gr.Textbox(
                    label="📌 Topic",
                    placeholder="Example: Trigonometry, Python loops"
                )

                quiz_subject = gr.Dropdown(
                    subjects,
                    value="General",
                    label="📚 Subject"
                )

                quiz_difficulty = gr.Radio(
                    ["LKG 🍼", "Easy 🙂", "Normal 📘", "Strict 😈"],
                    value="Normal 📘",
                    label="🎯 Difficulty"
                )

                quiz_language = gr.Dropdown(
                    list(languages.keys()),
                    value="English",
                    label="🌍 Language"
                )

                quiz_btn = gr.Button("🧪 Generate Quiz")

                quiz_output = gr.Textbox(
                    label="📝 Quiz Questions",
                    lines=16
                )

            quiz_btn.click(
                generate_quiz,
                inputs=[quiz_topic, quiz_subject, quiz_difficulty, quiz_language],
                outputs=quiz_output
            )

demo.launch(debug=True)
