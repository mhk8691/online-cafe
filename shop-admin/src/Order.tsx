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
  ShowButton,
} from "react-admin";
import { Stack } from "@mui/material";
import { useEffect, useState, ReactElement } from "react";
import { EditButton, Edit, SimpleForm } from "react-admin";

const CustomerFilters = [
  <SearchInput source="username" alwaysOn placeholder="customer name" />,
  <TextInput label="status" source="status" placeholder="status" />,
  <TextInput label="date" source="order_date" placeholder="date" />,
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
    <Datagrid>
      <TextField source="id" />
      <TextField source="username" />
      <DateField source="order_date" />
      <NumberField source="total_amount" />
      <TextField source="status" />
      <TextField source="quantity" />
      <EditButton label="edit" />
      <ShowButton label="show" />
    </Datagrid>
  </List>
);
