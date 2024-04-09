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
    <Datagrid>
      <TextField source="id" />
      <TextField source="username" />
      <DateField source="order_date" />
      <NumberField source="total_amount" />
      <TextField source="status" />
      <TextField source="quantity" />
      <EditButton label="" />
      <ShowButton label="" />
    </Datagrid>
  </List>
);
