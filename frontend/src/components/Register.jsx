import { useState } from "react";

import api from "../services/api";

function Register({ setTab }) {

  const [form, setForm] = useState({
    username: "",
    password: "",
    name: "",
    weight: "",
    height: "",
    goal: "",
    diet_preference: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const register = async () => {
    try {

      await api.post(
        "/auth/register",
        {
          ...form,
          weight: Number(form.weight),
          height: Number(form.height)
        }
      );

      alert("Registration Successful");

setTab("login");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Registration Failed"
      );

    }
  };
return (
  <div>

      <h2>Register</h2>

      <input
        name="username"
        placeholder="Username"
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="password"
        type="password"
        placeholder="Password"
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="name"
        placeholder="Name"
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="weight"
        placeholder="Weight"
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="height"
        placeholder="Height"
        onChange={handleChange}
      />

      <br /><br />

      <select
  name="goal"
  onChange={handleChange}
>

  <option value="">
    Select Goal
  </option>

  <option value="Weight Loss">
    Weight Loss
  </option>

  <option value="Muscle Gain">
    Muscle Gain
  </option>

  <option value="Maintain Fitness">
    Maintain Fitness
  </option>

</select>

      <br /><br />

     <select
  name="diet_preference"
  onChange={handleChange}
>

  <option value="">
    Select Diet Preference
  </option>

  <option value="Vegetarian">
    Vegetarian
  </option>

  <option value="Vegan">
    Vegan
  </option>

  <option value="Non Vegetarian">
    Non Vegetarian
  </option>

</select>

      <br /><br />

      <button onClick={register}>
        Register
      </button>

    </div>
  );
}

export default Register;