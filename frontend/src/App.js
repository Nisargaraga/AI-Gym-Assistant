import { HashRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import Auth from "./components/Auth";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/app" element={<Layout />} />
      </Routes>
    </HashRouter>
  );
}

export default App;
