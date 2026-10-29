import { useState } from "react";
import { getHealth } from "./services/api";

function App() {
  const [status, setStatus] = useState("idle");
  const [message, setMessage] = useState("");

  async function checkHealth() {
    setStatus("loading");
    try {
      const data = await getHealth();
      setMessage(data.status);
      setStatus("success");
    } catch (err) {
      setMessage(err.message);
      setStatus("error");
    }
  }

  return (
    <div>
      <h1>RepoPilot</h1>
      <p>Understand any codebase, faster.</p>
      <button onClick={checkHealth} disabled={status === "loading"}>
        {status === "loading" ? "Checking..." : "Check backend"}
      </button>
      {status === "success" && <p>Backend says: {message}</p>}
      {status === "error" && <p>Could not reach backend: {message}</p>}
    </div>
  );
}

export default App;