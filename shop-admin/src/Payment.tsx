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
} from "react-admin";
import { Stack } from "@mui/material";

const CustomerFilters = [
  <SearchInput source="name" alwaysOn />,
  <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={CustomerFilters} />
    <div>
      <FilterButton filters={CustomerFilters} />
      <CreateButton />
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
      <DateField source="payment_date" />
      {/* <ImageField source="picture" /> */}
    </Datagrid>
  </List>
);
