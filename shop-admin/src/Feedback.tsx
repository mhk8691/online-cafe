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

const FeedbackFilters = [
  <SearchInput source="order_id" alwaysOn placeholder="order id" />,
  <TextInput label="customer name" source="username" placeholder="customer name" />,
  <TextInput label="rating" source="rating" placeholder="rating" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={FeedbackFilters} />
    <div>
      <FilterButton filters={FeedbackFilters} />
    </div>
  </Stack>
);
export const FeedbackList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="show">
      <NumberField source="id" />
      <TextField source="customer_name" />
      <TextField source="order_id" />
      <NumberField source="rating" />
      <TextField source="comment" />
      <DateField source="feedback_date" />
      {/* <ImageField source="picture" /> */}
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
