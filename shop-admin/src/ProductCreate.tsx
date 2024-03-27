import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateField,
  required,
  FileInput,
  ImageField,
  SelectInput, // Assuming you have categories for selection
} from "react-admin";

export const ProductCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="name" validate={[required()]} fullWidth label="Name" />
      <TextInput
        source="description"
        multiline={true}
        label="Description"
        fullWidth
      />
      <TextInput source="price" multiline={true} label="Price" fullWidth />
      <SelectInput // Use SelectInput for category selection if applicable
        source="categories_id"
        label="Category"
        fullWidth
        choices={[
          // Replace with your category options
          { id: 1, name: "Category 1" },
          { id: 2, name: "Category 2" },
          { id: 3, name: "Category 3" },
          { id: 4, name: "Category 4" },
        ]}
      />
      <FileInput source="picture" label="Picture" accept="image/*" fullWidth />
    </SimpleForm>
  </Create>
);
