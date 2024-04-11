import { Admin, Resource, EditGuesser, ShowGuesser } from "react-admin";
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
import CustomEditGuesser from "./Custom";
import productEdit from "./productEdit";
import { Route } from "react-router-dom";

export const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
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
    <Resource name="Order_Details" list={OrderDetailsList}  />
    <Resource
      name="feedback"
      list={FeedbackList}
      show={ShowGuesser}
    />
  </Admin>
);
