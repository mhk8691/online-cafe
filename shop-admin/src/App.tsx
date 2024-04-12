import { Admin, Resource, EditGuesser, ShowGuesser, LayoutProps } from "react-admin";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { CustomersList } from "./Customers";
import { ProductList } from "./Products";
import { CustomerCreate } from "./CustomerCreate";
import { ProductCreate } from "./ProductCreate";
import { CategoriesList } from "./Categories";
import { CategoriesCreate } from "./CategoriesCreate";
import { ShippingList } from "./Shipping";
import { UserCreate } from "./UserCreate";
import { feedbackCreate } from "./Respond";
import { UserList } from "./User";
import { OrderList } from "./Order";
import { PaymentList } from "./Payment";
import { OrderDetailsList } from "./Order_Details";
import { FeedbackList } from "./Feedback";
import { LogList } from "./AdminLogs";
import { NotificationList } from "./Notification";
import CustomEditGuesser from "./Custom";
import productEdit from "./productEdit";
import { Route } from "react-router-dom";

import {  Layout } from "react-admin";

import { MyAppBar } from "./MyAppBar";
import { JSX } from "react/jsx-runtime";

const MyLayout = (props: JSX.IntrinsicAttributes & LayoutProps) => <Layout {...props} appBar={MyAppBar} />;






export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    layout={MyLayout}
    darkTheme={{ palette: { mode: "dark" } }}
    // darkTheme={darkTheme}
  >
    <Resource
      name="customer"
      list={CustomersList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={CustomerCreate}
    />
    <Resource
      name="product"
      list={ProductList}
      edit={productEdit}
      show={ShowGuesser}
      create={ProductCreate}
    />
    <Resource
      name="category"
      list={CategoriesList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={CategoriesCreate}
    />
    <Resource
      name="shipping"
      list={ShippingList}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="user"
      list={UserList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={UserCreate}
    />
    <Resource
      name="orders"
      list={OrderList}
      edit={CustomEditGuesser}
      show={ShowGuesser}
    />
    <Resource name="payment" list={PaymentList} show={ShowGuesser} />
    <Resource name="Order_Details" list={OrderDetailsList} />
    <Resource name="feedback" list={FeedbackList} show={ShowGuesser} />
    <Resource name="admin_logs" list={LogList} show={ShowGuesser} />

    <Resource
      name="Notification"
      list={NotificationList}
      show={ShowGuesser}
      create={feedbackCreate}
    />
  </Admin>
);
