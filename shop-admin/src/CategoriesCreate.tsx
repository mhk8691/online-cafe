import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateField,
  required,
  FileInput,
  ImageField,
  SelectInput,
  NumberInput, // Assuming you have categories for selection
} from "react-admin";

export const CategoriesCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="name" validate={[required()]} fullWidth label="Name" />
      <TextInput
        source="description"
        multiline={true}
        label="Description"
        fullWidth
      />
      <NumberInput
        source="parent_category_id"
        multiline={true}
        label="Parent_category_id"
        fullWidth
      />

      <FileInput source="picture" label="Picture" accept="image/*" fullWidth />
    </SimpleForm>
  </Create>
);
