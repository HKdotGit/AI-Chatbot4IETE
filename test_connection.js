/**
 * Connection validation script for IETE-SF AI Chatbot.
 * Tests connection to the Google Gemini API.
 */
require('dotenv').config();

const DEFAULT_API_KEY = "YOUR_API_KEY_HERE";
const apiKey = process.env.GEMINI_API_KEY || DEFAULT_API_KEY;

async function testConnection() {
  console.log("Checking connection to Gemini API...");
  console.log(`Using API Key: ${apiKey.substring(0, 6)}...${apiKey.substring(apiKey.length - 4)}`);

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [
          { role: 'user', parts: [{ text: 'Respond with the word "Connected!" if you can read this.' }] }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP Error Status: ${response.status}`);
    }

    const data = await response.json();
    if (data.candidates && data.candidates[0].content.parts[0].text) {
      console.log("\x1b[32m%s\x1b[0m", "✔ Connection Successful!");
      console.log(`Response from Gemini: "${data.candidates[0].content.parts[0].text.trim()}"`);
    } else {
      console.log("\x1b[31m%s\x1b[0m", "✘ Unexpected response structure from Gemini API.");
      console.log(JSON.stringify(data, null, 2));
    }
  } catch (err) {
    console.error("\x1b[31m%s\x1b[0m", "✘ Connection Failed!");
    console.error(err.message);
    process.exit(1);
  }
}

testConnection();
