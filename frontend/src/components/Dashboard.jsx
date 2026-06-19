import { useEffect, useState } from "react";
import api from "../services/api";
import Recommendations
from "./Recommendations";
function Dashboard() {

  const [stats, setStats] = useState(null);

  const user =
    localStorage.getItem("user_name");

  useEffect(() => {

    const loadStats = async () => {

      const user_id =
        Number(localStorage.getItem("user_id"));

      try {

        const res = await api.get(
          `/analytics/${user_id}`
        );

        setStats(res.data);

      } catch {

        console.log("Analytics load failed");

      }
    };

    loadStats();

  }, []);

  return (

    <div>

      <h1>
        Welcome back, {user} 👋
      </h1>

      <p>
        Your AI fitness ecosystem is ready.
      </p>

      {stats && (

        <div className="stats">

          <div className="stat-card">
            <h1>🏋</h1>
            <h2>{stats.total_workouts}</h2>
            <p>Total Workouts</p>
          </div>

          <div className="stat-card">
            <h1>📈</h1>
            <h2>{stats.average_accuracy}%</h2>
            <p>Average Accuracy</p>
          </div>

          <div className="stat-card">
            <h1>🔥</h1>
            <h2>{stats.habit_records}</h2>
            <p>Habit Records</p>
          </div>

          <div className="stat-card">
            <h1>🎯</h1>
            <h2>{stats.goal}</h2>
            <p>Current Goal</p>
          </div>

        </div>

      )}
      <Recommendations />

    </div>

  );
}

export default Dashboard;