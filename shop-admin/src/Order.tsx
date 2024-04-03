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
import { useEffect, useState } from "react";

const CustomerFilters = [
  <SearchInput source="name" alwaysOn />,
  <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={CustomerFilters} />
    <div>
      <FilterButton filters={CustomerFilters} />
    </div>
  </Stack>
);

export const OrderList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="username" />
      <DateField source="order_date" />
      <NumberField source="total_amount" />
      <TextField source="status" />
      <TextField source="quantity" />
    </Datagrid>
  </List>
);
