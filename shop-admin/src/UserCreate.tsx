import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
  SelectInput,
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
      
      <SelectInput
        source="role"
        choices={[
          { id: "Admin", name: "Admin" },
          { id: "RegularAdmin", name: "RegularAdmin"}
        ]}
      />
    </SimpleForm>
  </Create>
);
