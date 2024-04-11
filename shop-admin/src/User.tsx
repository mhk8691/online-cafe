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
  EditButton,
  ShowButton,
} from "react-admin";
import { Stack } from "@mui/material";

const CustomerFilters = [
  <SearchInput source="username" alwaysOn placeholder="username" />,
  <TextInput label="role" source="role" />,
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
export const UserList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="username" />
      <TextField source="password" />
      <EmailField source="email" />
      <TextField source="role" />
      <EditButton label="edit" />
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
