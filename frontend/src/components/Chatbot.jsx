import { useState } from "react";
import api from "../services/api";

function Chatbot() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {

    if (!message.trim()) return;

    try {

      const res = await api.post(
        `/chatbot/message?message=${message}`
      );

      setChat([
        ...chat,
        {
          user: message,
          bot: res.data.reply
        }
      ]);

      setMessage("");

    } catch {

      alert("Chatbot Error");

    }
  };

  return (

  <div className="page-container">

    <div className="card">

      <h2>🤖 AI Gym Buddy</h2>

      <div className="chat-box">

        {chat.map((item, index) => (

          <div key={index}>

            <div className="user-msg">
              👤 {item.user}
            </div>

            <div className="bot-msg">
              🤖 {item.bot}
            </div>

          </div>

        ))}

      </div>

      <br />

      <input
        placeholder="Ask about diet, workouts, motivation..."
        value={message}
        onChange={(e)=>
          setMessage(e.target.value)
        }
      />

      <button onClick={sendMessage}>
        Send
      </button>

       </div>

  </div>
);
}

export default Chatbot;