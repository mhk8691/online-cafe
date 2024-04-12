import { AppBar, RefreshButton, TitlePortal, ToggleThemeButton } from "react-admin";
import SettingsIcon from "@mui/icons-material/Settings";
import { IconButton } from "@mui/material";

const SettingsButton = () => (
  <IconButton color="inherit">
    <SettingsIcon />
  </IconButton>
);

export const MyAppBar = () => (
  <AppBar>
    <TitlePortal />
    <SettingsButton />
    <AppBar toolbar={<ToggleThemeButton />} />
  </AppBar>
);
