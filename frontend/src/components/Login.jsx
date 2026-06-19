import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const login = async () => {

    try {

      const res = await api.post(
        "/auth/login",
        {
          username,
          password
        }
      );

      localStorage.setItem(
        "user_id",
        res.data.user_id
      );
      localStorage.setItem(
  "user_name",
  res.data.name
);
localStorage.setItem(
  "goal",
  res.data.goal
);
      navigate("/app");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Login Failed"
      );

    }
  };

  return (
  <div>

      <h2>Login</h2>

      <input
        placeholder="Username"
        onChange={(e)=>
          setUsername(e.target.value)
        }
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>
          setPassword(e.target.value)
        }
      />

      <br /><br />

      <button onClick={login}>
        Login
      </button>

    </div>
  );
}

export default Login;