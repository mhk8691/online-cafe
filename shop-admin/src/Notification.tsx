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

const FeedbackFilters = [
  <SearchInput source="message" alwaysOn placeholder="message" />,
  <TextInput
    label="status"
    source="status"
    placeholder="status"
  />,
  <TextInput label="date" source="created_at" placeholder="date" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={FeedbackFilters} />
    <div>
      <FilterButton filters={FeedbackFilters} />
    </div>
  </Stack>
);
export const NotificationList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="create">
      <NumberField source="id" />
      <TextField source="customer_id" />
      <TextField source="message" />
      <NumberField source="created_at" />
      <TextField source="status" />
      
      <ShowButton label="show" />
      <DeleteButton label="delete" />
    </Datagrid>
  </List>
);
