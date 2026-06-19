import { useState } from "react";
import api from "../services/api";

function Analytics() {

  const [data, setData] = useState(null);

  const loadAnalytics = async () => {

    const user_id =
      Number(localStorage.getItem("user_id"));

    try {

      const res = await api.get(
        `/analytics/${user_id}`
      );

      setData(res.data);

    } catch {

      alert("Analytics Error");

    }
  };

  return (

  <div className="page-container">

    <div className="card">

      <h2>Analytics</h2>

      <button onClick={loadAnalytics}>
        Load Analytics
      </button>

      <br /><br />

      {data &&
      <div>

  <h3>Name: {data.name}</h3>

  <h3>Goal: {data.goal}</h3>

  <h3>
    Total Workouts:
    {data.total_workouts}
  </h3>

  <h3>
    Average Accuracy:
    {data.average_accuracy}%
  </h3>

  <h3>
    Habit Records:
    {data.habit_records}
  </h3>

</div>
      }

     </div>

  </div>
  );
}

export default Analytics;