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
import { blob } from "stream/consumers";

const CustomerFilters = [<SearchInput source="category_name" alwaysOn />];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={CustomerFilters} />
  </Stack>
);
export const CategoriesList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <NumberField source="id" />
      <TextField source="name" />
      <NumberField source="parent_category_id" />
      <DateField source="created_at" />
      <TextField source="description" />
      <ImageField source="picture" />
      <EditButton label="Edit" />
      <ShowButton label="Show" />
    </Datagrid>
  </List>
);
