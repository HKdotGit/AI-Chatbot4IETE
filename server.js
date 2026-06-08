const express = require('express');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
app.use(express.json());

// Fallback API key to run out-of-the-box (matching index.html)
const DEFAULT_API_KEY = "AIzaSyCEIeNfyQFj_wG0tiXf7wNXx-wX5sDs1qo";
const apiKey = process.env.GEMINI_API_KEY || DEFAULT_API_KEY;

// Serve static assets from current directory
app.use(express.static(path.join(__dirname, '.')));

// Function to construct system instruction prompt from database.json
function generateSystemInstruction() {
  const dbPath = path.join(__dirname, 'data', 'database.json');
  if (!fs.existsSync(dbPath)) {
    console.warn("Warning: Database file not found. System instructions empty.");
    return "";
  }
  
  try {
    const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
    const org = db.organization || {};
    const stats = db.statistics || {};
    const values = db.core_values || [];
    const events = db.events || [];
    const team = db.team_structure || {};
    const supercore = team.supercore || {};
    const departments = team.departments || [];

    let lines = [];
    lines.push("You are the official IETE-SF AI Chatbot. Your primary role is to provide information about the tech community IETE-SF MPSTME based on the following official database.");
    lines.push("[IETE-SF DATABASE START]");
    lines.push(`Motto: ${org.motto || 'For the Engineers, By the Engineers'}.`);
    lines.push(`About: ${org.about || ''}`);
    lines.push(`Stats: ${stats.members || '220+'} Team Members, ${stats.incentives || '100K+'} Incentives, ${stats.alumni || '1,200+'} Alumni, ${stats.followers || '2,500+'} Followers.`);
    
    lines.push("Mission Core Values:");
    values.forEach(v => lines.push(`- ${v.name}: ${v.description}`));
    
    lines.push("Events:");
    events.forEach(e => lines.push(`- ${e.name}: ${e.description}`));
    
    lines.push("\nTeam Structure & Departments:");
    lines.push("Supercore:");
    Object.entries(supercore).forEach(([role, name]) => {
      const roleTitle = role.replace(/_/g, '-').split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('-');
      lines.push(`- ${roleTitle}: ${name}`);
    });
    
    lines.push("\nDepartments & Heads:");
    departments.forEach(dept => {
      const heads = (dept.heads || []).join(', ');
      const subheads = (dept.sub_heads || []).join(', ');
      lines.push(`- ${dept.name}: ${heads} (Sub-Heads: ${subheads})`);
    });
    
    lines.push("\nGeneral Info & Contact:");
    lines.push(`- Website: ${org.website}`);
    lines.push(`- Established: ${org.established}`);
    lines.push(`- Email: ${org.email}`);
    lines.push(`- Location: ${org.location}`);
    lines.push(`- Faculty Mentors: ${(org.faculty_mentors || []).join(', ')}`);
    lines.push("[IETE-SF DATABASE END]");
    
    lines.push(`
Rules:
1. When asked about IETE-SF, answer gracefully and enthusiastically using the database above. If asked who you are, introduce yourself.
2. Provide concise, friendly answers and format them beautifully using markdown.
3. You are a highly versatile AI. If asked about general tech, coding, or any topics unrelated to IETE-SF, seamlessly answer them utilizing your broader Gemini knowledge base. Do not force the conversation back to IETE-SF or sound overly self-centered about the organization.`);

    return lines.join('\n');
  } catch (err) {
    console.error("Error reading or parsing database.json:", err);
    return "";
  }
}

const SYSTEM_INSTRUCTION = generateSystemInstruction();

// Serve root webpage
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Proxy Chat Endpoint
app.post('/api/chat', async (req, res) => {
  const { contents } = req.body;
  if (!contents) {
    return res.status(400).json({ error: "Missing 'contents' in request body" });
  }

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: contents,
        systemInstruction: {
          parts: [{ text: SYSTEM_INSTRUCTION }]
        }
      })
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Gemini API Error (${response.status}): ${errText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error communicating with Gemini API:", error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 5000;
const HOST = process.env.HOST || '127.0.0.1';
app.listen(PORT, HOST, () => {
  console.log(`IETE-SF Chatbot backend running on http://${HOST}:${PORT}`);
});
