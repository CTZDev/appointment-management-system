import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import AppointmentApp from "./AppointmentApp.tsx";
import "./styles/global/index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppointmentApp />
  </StrictMode>
);
