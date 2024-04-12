import { AppBar, Logout, RefreshButton, TitlePortal, ToggleThemeButton } from "react-admin";
import SettingsIcon from "@mui/icons-material/Settings";
import { IconButton } from "@mui/material";
import React from "react";
const SettingsButton = () => (
  <IconButton color="inherit">
    <SettingsIcon />
  </IconButton>
);
import { Link } from "react-router-dom";




const LogoutButton: React.FC = () => {
  const handleLogout = () => {
    // اینجا باید اقدامات لازم برای خروج از سیستم را انجام دهید، مانند حذف توکن احراز هویت از local storage و غیره.
    console.log("User logged out");
  };

  return (
    <Link to="http://localhost:5000/login-admin" onClick={handleLogout}>
      Logout
    </Link>
  );
};

export default LogoutButton;



export const MyAppBar = () => (
  <AppBar>
    <TitlePortal />
    <LogoutButton />
  </AppBar>
);

