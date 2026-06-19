import api from "../services/api";

function Habits() {

  const trackHabit = async () => {

    const user_id =
      Number(localStorage.getItem("user_id"));

    try {

      await api.post(
        "/habits/track",
        {
          user_id,
          streak: 5,
          missed_days: 1,
          prediction: "Consistent"
        }
      );

      alert("Habit Saved");

    } catch {

      alert("Habit Error");

    }
  };

  return (

    <div className="page-container">

      <div className="card">

        <h2>Habit Tracker</h2>

        <button onClick={trackHabit}>
          Save Habit
        </button>

      </div>

    </div>
  );
}

export default Habits;