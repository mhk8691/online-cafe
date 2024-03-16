import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
} from "react-admin";

export const product = () => (
  <Create>
    <SimpleForm>
      <TextInput source="name" validate={[required()]} fullWidth />
      <TextInput source="desc" multiline={true} label="desc" fullWidth />
      <TextInput source="price" multiline={true} label="price" fullWidth />
    </SimpleForm>
  </Create>
);
