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

export const OrderDetailsList = () => (
  <List>
    <ListToolbar />
    <Datagrid>
      <TextField source="id" />
      <TextField source="order_id" />
      <TextField source="product_name" />
      <NumberField source="quantity" />
      <NumberField source="unit_price" />
    </Datagrid>
  </List>
);
