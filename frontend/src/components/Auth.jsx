import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

function Auth() {

  const [tab, setTab] = useState("login");

 return (

  <div className="auth-container">

    <div className="card">

      <h1>🏋 AI Gym Assistant</h1>

      <div>

        <button
          onClick={() => setTab("login")}
        >
          Login
        </button>

        <button
          onClick={() => setTab("register")}
        >
          Register
        </button>

      </div>

      <br />

      {
        tab === "login"
  ? <Login />
  : <Register setTab={setTab} />
      }

    </div>

  </div>
);
}

export default Auth;