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
      <CreateButton />
    </div>
  </Stack>
);

export const ProductList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <NumberField source="id" />
      <TextField source="name" />
      <NumberField source="price" />
      <TextField source="description" />
      <TextField source="categories_name" />

      <ImageField
        source="picture"
        sx={{
          "& img": {
            maxWidth: 100,
            maxHeight: 100,
            objectFit: "contain",
          },
        }}
      />
    </Datagrid>
  </List>
);
