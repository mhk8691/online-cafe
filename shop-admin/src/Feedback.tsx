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

const FeedbackFilters = [
  <SearchInput source="name" alwaysOn />,
  <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
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
    </Datagrid>
  </List>
);
