import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
} from "react-admin";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { CustomersList } from "./Customers";
import { CustomerCreate } from "./CustomerCreate";
import { product } from "./product";

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
      list={CustomersList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={product}
    />
  </Admin>
);
