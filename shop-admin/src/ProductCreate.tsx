import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateField,
  required,
  FileInput,
  ImageField,
  ImageInput,
  SelectInput, // Assuming you have categories for selection
} from "react-admin";
import data from "./category.json";
let category = data.category;

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
        choices={category.map((item) => ({
          id: item.category_id,
          name: item.category_name,
        }))}
      />

      {/* جایگزین کردن */}
      <ImageInput source="pictures" label="Related pictures"></ImageInput>
    </SimpleForm>
  </Create>
);
