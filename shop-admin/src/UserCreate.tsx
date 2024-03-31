import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
} from "react-admin";

export const UserCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="username" validate={[required()]} fullWidth />

      <TextInput
        source="password"
        multiline={true}
        label="password"
        fullWidth
      />
      <TextInput source="email" multiline={true} label="email" fullWidth />
      <TextInput source="role" multiline={true} label="role" fullWidth />
    </SimpleForm>
  </Create>
);
