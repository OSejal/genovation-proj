# 🌟 Genovation — AI Prompt Execution API

###  A FastAPI-based backend that supports user authentication, Replicate model inference, and secure prompt execution through REST APIs.

### Features:
1. Token-based user authentication
2. AI model integration (Replicate)
3. `/prompt/` endpoint for LLM response generation
4. Secret keys loaded from `.env`
5. Modular service architecture (auth, routes, model services)


### Project Structure:

<pre>
genovation-repo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── models.py
│   ├── services.py
│   └── storage.py
├── .env
├── .gitignore
├── history.json
├── requirements.txt
└── README.md
</pre>

### Setup & Installation

1. Clone the Repository:
```bash
git clone https://github.com/<your-username>/genovation.git
cd genovation
```
2. Create Virtual Environment:
```bash
python -m venv venv
```

3. Activate Environment:

Windows:   

```bash
venv\Scripts\activate
```

Mac / Linux:  
```bash
source venv/bin/activate
```
4. Install Dependencies:  
```bash 
pip install -r requirements.txt
```
### Environment Variables
  
#####  Create a `.env` file in the project root:

```ini 
  REPLICATE_API_KEY=your_replicate_api_key_here
  
  REPLICATE_API_URL=https://api.replicate.com/v1/
  
  MODEL_VERSION=meta/meta-llama-3.1-405b-instruct
```

⚠️ Never commit `.env` to GitHub.
Ensure `.gitignore` contains:

```bash
  .env
```
 Running the Application:
```bash
  uvicorn app.main:app --reload
```

Server will start at: 
```bash
http://127.0.0.1:8000
```

### Authentication Flow 

#### 1️⃣Login to Get Token:

##### POST `/login/`

  Body:

  ```json
  {
    "username": "user1",
    "password": "pass1"
  }
```

Response:
  ```json
  {
    "token": "token_user1_abc123"
  }
```

You must send this token in all `/prompt` requests.

### Send Prompt to Model
#### 2️⃣Make a Prompt Request:

##### POST `/prompt/`

  PowerShell:

   ```powershell
  $headers = @{
    "Authorization" = "Bearer token_user1_abc123"
  }

  Invoke-RestMethod -Uri "http://127.0.0.1:8000/prompt/" `
    -Method POST `
    -Headers $headers `
    -Body '{"prompt": "Say hello!"}'
```

curl:

```bash
  curl -X POST http://127.0.0.1:8000/prompt/ \
  -H "Authorization: Bearer token_user1_abc123" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say hello!"}'
```

#### Example Response:

```json
{
  "response": "Hello! How can I assist you today?"
}
```