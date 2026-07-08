import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";

export default function Layout() {
  return (
    <div className="appShell">
      <Sidebar />
      <main className="mainArea">
        <Header />
        <Outlet />
      </main>
    </div>
  );
}
