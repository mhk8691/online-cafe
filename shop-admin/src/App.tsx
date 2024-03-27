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
import { ProductList } from "./Products";
import { CustomerCreate } from "./CustomerCreate";
import { ProductCreate } from "./ProductCreate";
import { CategoriesList } from "./Categories";
import { CategoriesCreate } from "./CategoriesCreate";

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
      edit={EditGuesser}
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
  </Admin>
);