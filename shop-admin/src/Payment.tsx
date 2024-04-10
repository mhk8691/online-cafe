import {
  CreateButton,
  Datagrid,
  FilterButton,
  FilterForm,
  ListBase,
  List,
  Pagination,
  TextField,
  TextInput,
  SearchInput,
  EmailField,
  NumberField,
  DateField,
  ImageField,
  EditButton,
  ShowButton,
} from "react-admin";
import { Stack } from "@mui/material";

const PaymentFilters = [
  <SearchInput source="order_id" alwaysOn placeholder="order number" />,
  <TextInput
    label="payment method"
    source="payment_method"
    placeholder="payment method"
  />,
  <TextInput label="date" source="payment_date" placeholder="date" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={PaymentFilters} />
    <div>
      <FilterButton filters={PaymentFilters} />
    </div>
  </Stack>
);
export const PaymentList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="show">
      <NumberField source="id" />
      <TextField source="order_id" />
      <TextField source="payment_method" />
      <NumberField source="amount" />
      <DateField source="payment_date"/>
      {/* <ImageField source="picture" /> */}
      <ShowButton label="" />
    </Datagrid>
  </List>
);
