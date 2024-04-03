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
export const ShippingList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="customer_id" />
      <TextField source="recipient_name" />
      <TextField source="address_line1" />
      <TextField source="address_line2" />
      <TextField source="city" />
      <TextField source="state" />
      <TextField source="postal_code" />
      <TextField source="country" />
    </Datagrid>
  </List>
);
