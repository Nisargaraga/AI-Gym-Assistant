import { useEffect, useState } from "react";
import api from "../services/api";

function Profile() {

  const [profile, setProfile] =
    useState(null);

  useEffect(() => {

    const loadProfile = async () => {

      const user_id =
        Number(
          localStorage.getItem("user_id")
        );

      try {

        const res = await api.get(
          `/auth/profile/${user_id}`
        );

        setProfile(res.data);

      } catch {

        alert("Profile Error");

      }
    };

    loadProfile();

  }, []);

  if (!profile)
    return <div>Loading...</div>;

 return (

  <div className="page-container">

    <div className="card">

      <h1>👤 My Profile</h1>

      <hr />

      <h3>👤 {profile.name}</h3>

      <h3>
        📧 {profile.username}
      </h3>

      <h3>
        ⚖ {profile.weight} kg
      </h3>

      <h3>
        📏 {profile.height} cm
      </h3>

      <h3>
        🎯 {profile.goal}
      </h3>

      <h3>
        🥗 {profile.diet_preference}
      </h3>

        </div>

  </div>
);
}

export default Profile;