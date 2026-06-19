import { useEffect, useState } from "react";
import api from "../services/api";

function Admin() {

  const [stats, setStats] =
    useState(null);

  useEffect(() => {

    const loadStats = async () => {

      const res = await api.get(
        "/admin/stats"
      );

      setStats(res.data);
    };

    loadStats();

  }, []);

  if (!stats)
    return <div>Loading...</div>;

  return (

    <div className="card">

      <h2>Admin Dashboard</h2>

      <h3>
        Users:
        {stats.total_users}
      </h3>

      <h3>
        Workouts:
        {stats.total_workouts}
      </h3>

      <h3>
        Habits:
        {stats.total_habits}
      </h3>

    </div>

  );
}

export default Admin;