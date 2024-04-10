import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
} from "react-admin";

export const feedbackCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="message" validate={[required()]} fullWidth />
    </SimpleForm>
  </Create>
);
