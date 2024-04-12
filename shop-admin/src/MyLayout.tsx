import { Layout, LayoutProps } from "react-admin";

import { MyAppBar } from "./MyAppBar";
import { JSX } from "react/jsx-runtime";

export const MyLayout = (props: JSX.IntrinsicAttributes & LayoutProps) => <Layout {...props} appBar={MyAppBar} />;
