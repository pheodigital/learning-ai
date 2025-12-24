require("dotenv").config(); // Load .env at top

const readline = require("readline");
const { LangflowClient } = require("@datastax/langflow-client");

// Load from .env
const API_KEY = process.env.LANGFLOW_API_KEY;
const SERVER = process.env.LANGFLOW_SERVER;
const FLOW_ID = process.env.FLOW_ID;

// Validate env vars
if (!API_KEY || !SERVER || !FLOW_ID) {
  console.error(
    "❌ Missing required env vars: LANGFLOW_API_KEY, LANGFLOW_SERVER, FLOW_ID"
  );
  console.log(
    "Create .env file with your values from Langflow > Share > API access"
  );
  process.exit(1);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const client = new LangflowClient({
  baseUrl: SERVER,
  apiKey: API_KEY,
});

async function sendMessage(message) {
  try {
    const response = await client.flow(FLOW_ID).run(message, {
      session_id: "user_1",
    });
    return response.chatOutputText() || "No response";
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

function chat() {
  console.log('🤖 Langflow RAG Chatbot (type "quit" to exit)\n');
  const ask = () => {
    rl.question("👤 You: ", async (input) => {
      if (["quit", "exit", "bye"].includes(input.trim().toLowerCase())) {
        console.log("👋 Goodbye!");
        rl.close();
        return;
      }
      const response = await sendMessage(input.trim());
      console.log(`🤖 Assistant: ${response}\n`);
      ask();
    });
  };
  ask();
}

chat();
