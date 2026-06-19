function Recommendations() {

  const goal =
    localStorage.getItem("goal");

  let workouts = [];

  if (goal === "Weight Loss") {

    workouts = [
      "20 Squats",
      "15 Lunges",
      "30 Jumping Jacks",
      "15 Min Walking"
    ];

  } else if (
    goal === "Muscle Gain"
  ) {

    workouts = [
      "15 Pushups",
      "20 Squats",
      "10 Pullups",
      "30 Sec Plank"
    ];

  } else {

    workouts = [
      "15 Squats",
      "15 Pushups",
      "10 Min Walk"
    ];

  }

  return (

    <div className="card">

      <h2>
        🎯 Today's Recommendation
      </h2>

      <ul>

        {workouts.map((item, index) => (

          <li key={index}>
            {item}
          </li>

        ))}

      </ul>

    </div>

  );
}

export default Recommendations;