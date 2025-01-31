import { BrowserRouter, Routes, Route } from "react-router-dom";

import { ThemeProvider } from "@/components/theme-provider";
import NavBar from "./components/NavBar";

import "./App.css";

import Home from "./components/Home";
import ReviewSubmissions from "./components/ReviewSubmissions";
import AddSubmissions from "./components/AddSubmissions";
import Contributors from "./components/Contributors";
import About from "./components/About";
import PastPapers from "./components/PastPapers";

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/review-submissions" element={<ReviewSubmissions />} />
          <Route path="/add-submissions" element={<AddSubmissions />} />
          <Route path="/contributors" element={<Contributors />} />
          <Route path="/about" element={<About />} />
          <Route path="/past-papers" element={<PastPapers />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
