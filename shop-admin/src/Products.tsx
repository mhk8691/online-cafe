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
  SelectField,
  EditButton,
  ShowButton,
  ChipField,
  DeleteButton,
} from "react-admin";
import { Stack } from "@mui/material";
import { useEffect, useState } from "react";

const ProductFilters = [
  <SearchInput source="name" alwaysOn placeholder="product name" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={ProductFilters} />
  </Stack>
);

export const ProductList = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <NumberField source="id" />
      <TextField source="name" />
      {/* <TextField source="category_name" /> */}
      <ChipField source="category_name" />
      <NumberField source="price" />
      <TextField source="description" />

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
      <EditButton label="Edit" />
      <ShowButton label="Show" />
      <DeleteButton label="delete" />
    </Datagrid>
  </List>
);
