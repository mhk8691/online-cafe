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
import { useEffect, useState } from "react";

const CustomerFilters = [
  <SearchInput source="name" alwaysOn placeholder="product name" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={CustomerFilters} />
  </Stack>
);

export const OrderDetailsList = () => (
  <List>
    <ListToolbar />
    <Datagrid>
      <TextField source="id" />
      <TextField source="order_id" />
      <TextField source="username" />
      <TextField source="product_name" />
      <NumberField source="quantity" />
      <NumberField source="unit_price" />
      <EditButton label="edit" />
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
