import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Dashboard from "./Dashboard";
import Diet from "./Diet";
import Workout from "./Workout";
import Habits from "./Habits";
import Analytics from "./Analytics";
import Chatbot from "./Chatbot";
import Profile from "./Profile";
import Admin from "./Admin";

function Layout() {
    const navigate = useNavigate();
    const logout = () => {

  localStorage.removeItem("user_id");
  localStorage.removeItem("user_name");

  navigate("/");

};

  const [active, setActive] =
    useState("dashboard");

  const renderPage = () => {

    switch(active) {
        case "profile":
  return <Profile />;

      case "diet":
        return <Diet />;

      case "workout":
        return <Workout />;

      case "habits":
        return <Habits />;

      case "analytics":
        return <Analytics />;

      case "chatbot":
        return <Chatbot />;

      case "admin":
        return <Admin />;

      default:
        return <Dashboard />;
        
    }
  };

  return (

    <div className="app-container">

      <div className="sidebar">

        <h2>🏋 AI Gym Assistant</h2>

<p>
  Welcome,
  <br />
  <b>
    {localStorage.getItem("user_name")}
  </b>
</p>

<hr />

        <button
          onClick={() =>
            setActive("dashboard")
          }
        >
          📊 Dashboard
        </button>

        <button
          onClick={() =>
            setActive("diet")
          }
        >
          🥗 Diet AI
        </button>

        <button
          onClick={() =>
            setActive("workout")
          }
        >
          🏋 Workout
        </button>

        <button
          onClick={() =>
            setActive("habits")
          }
        >
          🔥 Habits
        </button>

        <button
          onClick={() =>
            setActive("analytics")
          }
        >
          📈 Analytics
        </button>

        <button
          onClick={() =>
            setActive("chatbot")
          }
        >
          🤖 AI Buddy
          <hr />
       
</button>

   <button
  onClick={() =>
    setActive("profile")
  }
>
  👤 Profile
</button>
<button
  onClick={logout}
>
  🚪 Logout

</button>
<button
  onClick={() =>
    setActive("admin")
  }
>
  🛠 Admin
</button>
      </div>

      <div className="content">

        {renderPage()}

      </div>

    </div>

  );
}

export default Layout;