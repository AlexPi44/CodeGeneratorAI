# 🧠 AI Code Generator using AWS Bedrock + Claude

This is a simple yet powerful Python-based AI tool that generates code from text instructions using **Anthropic Claude (via AWS Bedrock)** and automatically saves the output to an **Amazon S3** bucket.

Ideal for serverless deployment on **AWS Lambda**, but also adaptable for local use.

---

## ✨ Features

- Uses Claude v2 on AWS Bedrock for natural code generation
- Input prompt: "Write Python code for reversing a list"
- Output: Saved as `.py` file in S3
- Fully serverless when deployed on Lambda
- Lightweight, fast, and scalable

---

## 📁 Files & Their Roles

| File | Purpose |
|------|---------|
| `code_generation.py` | Main script: generates code and saves it to S3 |
| `boto3Layer.script` | Bash script: creates a `boto3` Lambda layer |
| `boto3_layer.zip` | Pre-built layer to upload to AWS Lambda |
| `README.md` | Full setup and usage documentation |
| `requirements.txt` | Optional: Install locally for testing |
| `event_sample.json` | Sample event input for local testing |

---

## 🚀 How It Works

1. User sends a text prompt (e.g. “Build a login form in HTML”)
2. Claude AI processes the prompt and returns code
3. The code is stored as a `.py` file in your specified S3 bucket

---

## ⚙️ Setup Instructions (AWS Lambda)

### ✅ Prerequisites

- An AWS account with access to:
  - Bedrock
  - S3
  - Lambda
- An existing S3 bucket (or create one)
- Python 3.x environment (for local testing)

---

### 🛠️ Step 1: Create the Boto3 Lambda Layer

Run this command in your terminal (on Mac/Linux):
```bash
bash boto3Layer.script
```

This will:
- Create a virtual environment
- Install `boto3` into a `python/` directory
- Zip it into `boto3_layer.zip`

---

### 🧩 Step 2: Upload Layer to AWS Lambda

1. Go to AWS Console → Lambda → **Layers** → *Create layer*
2. Name it `boto3-layer`
3. Upload `boto3_layer.zip`
4. Select your Python runtime (e.g., Python 3.9)
5. After creating, go to your Lambda function → **Add layer** → select the one you just created

---

### 📜 Step 3: Deploy the Lambda Function

1. Create a new Lambda function
2. Paste the contents of `code_generation.py` into the Lambda code editor
3. Set the handler to:
```
lambda_handler
```
4. Set Python runtime (same as your layer, e.g. Python 3.9)
5. Attach your `boto3` layer to the function

---

### 🧠 Step 4: Configure Bedrock + S3

#### Inside `code_generation.py`, edit the following:
```python
s3_bucket = 'your-bucket-name'  # Replace with your real bucket
```

You can also change:
- AWS region: `us-west-2` → your region
- Model ID: e.g., `anthropic.claude-v2` → another Bedrock model

---

## 🧪 Testing the Function

Use the Lambda test tab or an API Gateway to send this payload:

```json
{
  "body": {
    "message": "Write a Python class for a calculator",
    "key": "Python"
  }
}
```

### ✅ Expected Result:
A new file appears in your S3 bucket under `code-output/HHMMSS.py`, containing Claude’s generated code.

---

## 🔁 Run Locally (Optional)

You can adapt the script for local use. Just simulate the Lambda input like this:

```python
event = {
    "body": json.dumps({
        "message": "Create a web server in Node.js",
        "key": "JavaScript"
    })
}

lambda_handler(event, None)
```

Make sure your local machine has:
```bash
pip install boto3
aws configure  # Add your credentials
```

---

## 📦 Project Improvements

- Add HTML/React front-end to collect prompt + display code
- Add support for multiple AI models (Claude, Jurassic, Titan, etc.)
- Return generated code via API (instead of only saving to S3)

---


## 📝 License

MIT License — Free to use and modify.
