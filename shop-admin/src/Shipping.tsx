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
  DeleteButton,
} from "react-admin";
import { Stack } from "@mui/material";

const CustomerFilters = [
  <SearchInput source="recipient_name" alwaysOn placeholder="recipient name" />,
  <TextInput label="city" source="city" />,
  <TextInput label="country" source="country" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={CustomerFilters} />
    <div>
      <FilterButton filters={CustomerFilters} />
    </div>
  </Stack>
);
export const ShippingList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="customer_name" />
      <TextField source="recipient_name" />
      <TextField source="address_line1" />
      <TextField source="address_line2" />
      <TextField source="city" />
      <TextField source="state" />
      <TextField source="postal_code" />
      <TextField source="country" />
      <EditButton label="Edit" />
      <ShowButton label="Show" />
      <DeleteButton label="delete" />
    </Datagrid>
  </List>
);
