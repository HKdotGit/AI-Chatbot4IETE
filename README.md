# IETE-SF AI Chatbot 🤖✨

> **"For the Engineers, By the Engineers"**

Welcome to the official **IETE-SF AI Chatbot** repository! This is an interactive chat application powered by Google's latest **Gemini 2.0 Flash** model, customized with a dynamic built-in knowledge database of **IETE-SF MPSTME** (Mukesh Patel School of Technology Management & Engineering, Mumbai).

The application is structured to support multiple ways of running: a zero-dependency standalone frontend, a Python Flask API server, a Node.js Express server, and a command-line interface (CLI) terminal chatbot.

---

## 🌟 Key Features

* **Direct Web Mode**: Run `index.html` directly in your browser with zero installations. It uses a client-side fetch mechanism.
* **Modern Premium UI/UX**: Built with HSL-tailored colors, dynamic typography, ambient gradients, typing indicators, glassmorphic elements, and full Markdown rendering.
* **Structured Data-Driven Core**:
  * All database details are stored cleanly in [data/database.json](data/database.json).
  * Backend components dynamically load system instructions from the structured database, separating data from application logic.
* **Multi-Backend support**:
  * **Python Flask Server**: Serves the frontend and proxies Gemini API requests securely.
  * **Node.js Express Server**: Serves the web assets and handles secure Gemini proxy routing.
* **Terminal CLI Chatbot**: Interactive terminal version using colored ANSI layouts for lightweight console chatting.
* **Data Processing & Validation**: Includes a dedicated validation and preprocessing pipeline to check the integrity of database records.

---

## 📂 Project Directory Structure

```text
├── data/
│   ├── database.json      # Structured IETE-SF records (events, members, values)
│   ├── faq.json           # General FAQ dataset for students
│   ├── database_summary.md# Auto-generated markdown report summarizing the database
│   └── process_data.py    # Python utility to validate and compile statistics
├── index.html             # Standalone responsive chatbot frontend (HTML/CSS/JS)
├── data_manager.py        # Python core class to load database records & build prompts
├── server.py              # Python Flask backend server & API Proxy
├── cli_chatbot.py         # Terminal command-line chatbot (Python)
├── requirements.txt       # Python dependency file
├── server.js              # Node.js Express backend server & API Proxy
├── test_connection.js     # Node.js utility to test Gemini API connection
├── package.json           # Node.js packages and scripts configuration
├── .env.example           # Reference template for API keys & server configs
└── .gitignore             # Rules for files ignored by Git (e.g. node_modules, .env)
```

---

## ⚙️ Quick Start Guide

### Option 1: Standalone Web Interface (Zero Installation)
Simply double-click the [index.html](index.html) file or open it in any web browser. 

---

### Setup Environment Variables (Optional but Recommended)
To secure your key or use a custom API Key, duplicate the `.env.example` file:
```bash
cp .env.example .env
```
Open `.env` and fill in your Gemini API Key:
```ini
GEMINI_API_KEY=your_actual_api_key_here
PORT=5000
```
*Note: If no API key is specified in `.env`, the servers will fall back to using the embedded default key to run out-of-the-box.*

---

### Option 2: Python Backend & CLI

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Validate & Inspect Database Data**:
   ```bash
   python data/process_data.py
   ```
   *This checks database.json integrity and outputs a `data/database_summary.md` file.*

3. **Run the Flask Server**:
   ```bash
   python server.py
   ```
   *Your server will start at `http://127.0.0.1:5000`. Open this URL in your browser to chat.*

4. **Run the Command Line Chatbot**:
   ```bash
   python cli_chatbot.py
   ```
   *Starts a conversational session directly in your terminal.*

---

### Option 3: Node.js / Express Backend

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Test Gemini Connection**:
   ```bash
   npm run test-conn
   ```

3. **Run the Express Server**:
   ```bash
   npm start
   ```
   *Your server will start at `http://127.0.0.1:5000`.*

---

## 🛠️ Built With

* **Frontend**: HTML5, CSS Custom Variables, Javascript (ES6+), FontAwesome Icons, Marked.js, Google Fonts (Outfit & Inter)
* **Python**: Flask, Python-dotenv, Google GenerativeAI SDK
* **Node.js**: Express, Dotenv, Gemini REST endpoint integration

---

## 🎓 About IETE-SF
**IETE-SF MPSTME** is a student branch of the Institution of Electronics and Telecommunication Engineers (IETE), established in **2013** at NMIMS MPSTME, Mumbai. It is a thriving technical community focused on cultivating a culture of tech innovation, design thinking, and collaborative learning among young engineering minds.
