import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";


import Layout from "./components/Layout";
import Auth from "./components/Auth";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Auth />}
        />

        <Route
          path="/app"
          element={<Layout />}
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;
