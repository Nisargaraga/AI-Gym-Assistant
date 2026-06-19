import { useState, useEffect } from "react";
import api from "../services/api";

function Workout() {

  const [exercise, setExercise] = useState("");
  const [reps, setReps] = useState("");
  const [history, setHistory] = useState([]);

  const user_id =
    Number(localStorage.getItem("user_id"));

  const loadHistory = async () => {

    try {

      const res = await api.get(
        `/workout/history/${user_id}`
      );

      setHistory(res.data);

    } catch {

      console.log("History Error");

    }
  };

  useEffect(() => {

  const fetchHistory = async () => {

    try {

      const res = await api.get(
        `/workout/history/${user_id}`
      );

      setHistory(res.data);

    } catch {

      console.log("History Error");

    }
  };

  fetchHistory();

}, [user_id]);

  const logWorkout = async () => {

    try {

      const res = await api.post(
        "/workout/log",
        {
          user_id,
          exercise,
          reps: Number(reps),
          accuracy: 90
        }
      );

      alert(
`Workout Logged

Score:
${res.data.performance_score}

Rating:
${res.data.rating}`
      );

      setExercise("");
      setReps("");

      loadHistory();

    } catch {

      alert("Workout Error");

    }
  };

  return (
    <div className="page-container">

      <div className="card">

        <h2>🏋 Workout Tracker</h2>

        <select
          value={exercise}
          onChange={(e) => setExercise(e.target.value)}
        >
          <option value="">Select Exercise</option>
          <option value="Pushups">Pushups</option>
          <option value="Squats">Squats</option>
          <option value="Lunges">Lunges</option>
          <option value="Plank">Plank</option>
          <option value="Burpees">Burpees</option>
          <option value="Jump Rope">Jump Rope</option>
        </select>

        <br /><br />

        <input
          placeholder="Reps"
          value={reps}
          onChange={(e) => setReps(e.target.value)}
        />

        <br /><br />

        <button onClick={logWorkout}>Log Workout</button>

        <hr />

        <h3>Workout History</h3>

        {history.length === 0 ? (
          <p>No workouts logged yet.</p>
        ) : (
          history.map((item) => (
            <div key={item.id} className="history-card">
              <h4>🏋 {item.exercise}</h4>
              <p>Reps: {item.reps}</p>
              <p>Accuracy: {item.accuracy}%</p>
            </div>
          ))
        )}

      </div>

    </div>
  );
}

export default Workout;