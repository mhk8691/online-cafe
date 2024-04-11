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
  <TextInput
    label="email"
    source="email"
    defaultValue="@gmail.com"
    placeholder="email"
  />,
  <TextInput label="phone" source="phone" placeholder="phone" />,
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

export const CustomersList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <NumberField source="id" />
      <TextField source="username" />
      <TextField source="password" />
      <EmailField source="email" />
      <TextField source="phone" />
      <EditButton label="edit" />
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
