import React from "react";
import { Edit, SimpleForm, TextInput, SelectInput } from "react-admin";
import data from "./category.json";
let category = data.category;
interface CustomEditProps {
  id: string;
  // status: string;

  // دیگر فیلدها
}

const CustomEdit: React.FC<CustomEditProps> = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="name" fullWidth label="Name" />
      <TextInput source="description" fullWidth label="description" />
      <TextInput source="price" fullWidth label="price" />

      <SelectInput // Use SelectInput for category selection if applicable
        source="categories_id"
        label="Category"
        fullWidth
        choices={category.map((item) => ({
          id: item.category_id,
          name: item.category_name,
        }))}
      />
    </SimpleForm>
  </Edit>
);

const CustomEditGuesser: React.FC<CustomEditProps> = (props) => (
  <CustomEdit {...props} />
);

export default CustomEditGuesser;
