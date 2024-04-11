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
  <SearchInput source="username" alwaysOn placeholder="username" />,
  <TextInput label="action" source="action" placeholder="action" />,
  <TextInput label="date" source="action_date" placeholder="date" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={PaymentFilters} />
    <div>
      <FilterButton filters={PaymentFilters} />
    </div>
  </Stack>
);
export const LogList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="show">
      <NumberField source="id" />
      <TextField source="username" />
      <TextField source="action" />
      <DateField source="action_date" />
      <NumberField source="ip_address" />
      {/* <ImageField source="picture" /> */}
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
