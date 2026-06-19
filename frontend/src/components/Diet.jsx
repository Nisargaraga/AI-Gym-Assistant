import api from "../services/api";
import { useState, useEffect } from "react";

function Diet() {

  const [diet, setDiet] = useState(null);
  const [profile, setProfile] = useState(null);

  useEffect(() => {

    const loadProfile = async () => {

      const user_id =
        Number(localStorage.getItem("user_id"));

      try {

        const res = await api.get(
          `/auth/profile/${user_id}`
        );

        setProfile(res.data);

      } catch {

        alert("Profile Load Failed");

      }
    };

    loadProfile();

  }, []);

  const generateDiet = async () => {

    try {

      const res = await api.post(
        "/diet/plan",
        null,
        {
          params: {
            weight: profile.weight,
            height: profile.height,
            goal: profile.goal,
            diet_preference:
              profile.diet_preference
          }
        }
      );

      setDiet(res.data);

    } catch {

      alert("Diet Generation Failed");

    }
  };

  if (!profile) return (
    <div className="page-container">
      <div className="card">Loading Profile...</div>
    </div>
  );

  return (

    <div className="page-container">
      <div className="card">

      <h2>🥗 AI Dietician</h2>

      <p>
        Goal: {profile.goal}
      </p>

      <p>
        Preference:
        {profile.diet_preference}
      </p>

      <button onClick={generateDiet}>
        Generate Diet Plan
      </button>

      <br /><br />

      {diet && (

        <div>

          <h3>
            BMI: {diet.BMI}
          </h3>

          <h3>
            Target Calories:
            {diet["Target Calories"]}
          </h3>

          <h4>Breakfast</h4>
          <p>
            {diet["Diet Plan"].breakfast}
          </p>

          <h4>Lunch</h4>
          <p>
            {diet["Diet Plan"].lunch}
          </p>

          <h4>Dinner</h4>
          <p>
            {diet["Diet Plan"].dinner}
          </p>

        </div>

      )}

      </div>
    </div>
  );

}

export default Diet;