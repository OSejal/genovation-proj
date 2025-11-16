🌟 Genovation — AI Prompt Execution API

A FastAPI-based backend that supports user authentication, Gemini/Replicate model inference, and secure prompt execution through REST APIs.

🚀 Features

🔐 Token-based user authentication

🤖 AI model integration (Gemini / Replicate)

⚡ /prompt/ endpoint for LLM response generation

🛡 Secret keys loaded from .env

🧰 Modular service architecture (auth, routes, model services)

📡 Works with PowerShell, curl, Postman

📁 Clean folder structure

📦 Project Structure
genovation-repo/
│── app/
│   ├── main.py
│   ├── auth.py
│   ├── services/
│   │   ├── gemini_service.py
│   │   └── replicate_service.py
│   ├── routers/
│   │   ├── auth_router.py
│   │   └── prompt_router.py
│   ├── models/
│   └── utils/
│
│── .env
│── .gitignore
│── requirements.txt
│── README.md

🔧 Setup & Installation
1. Clone the Repository
git clone https://github.com/<your-username>/genovation.git
cd genovation

2. Create Virtual Environment
python -m venv venv

3. Activate Environment

Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

🔐 Environment Variables

Create a .env file in the project root:

REPLICATE_API_KEY=your_replicate_api_key_here
REPLICATE_API_URL=https://api.replicate.com/v1/predictions
MODEL_VERSION=meta/meta-llama-3.1-405b-instruct

GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=models/gemini-1.5-flash


⚠️ Never commit .env to GitHub.
Ensure .gitignore contains:

.env

▶️ Running the Application
uvicorn app.main:app --reload


Server will start at:

http://127.0.0.1:8000

🔑 Authentication Flow
1️⃣ Login to Get Token

POST /login

Body:

{
  "username": "user1",
  "password": "pass1"
}


Response:

{
  "token": "token_user1_abc123"
}


You must send this token in all /prompt requests.

📨 Send Prompt to Model
2️⃣ Make a Prompt Request

POST /prompt/

PowerShell:

$headers = @{
  "Authorization" = "Bearer token_user1_abc123"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/prompt/" `
  -Method POST `
  -Headers $headers `
  -Body '{"prompt": "Say hello!"}'


curl:

curl -X POST http://127.0.0.1:8000/prompt/ \
-H "Authorization: Bearer token_user1_abc123" \
-H "Content-Type: application/json" \
-d '{"prompt": "Say hello!"}'


Example Response:

{
  "response": "Hello! How can I assist you today?"
}

🧠 Example JSON Response Structure
Success: