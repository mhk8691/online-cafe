import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
  NumberInput,
} from "react-admin";

export const ShippingCreate = () => (
  <Create>
    <SimpleForm>
      <NumberInput
        source="customer_id"
        multiline={true}
        label="customer_id"
        fullWidth
      />
      <TextInput
        source="recipient_name"
        multiline={true}
        label="recipient_name"
        fullWidth
      />
      <TextInput source="address_line1" fullWidth label="address_line1" />
      <TextInput source="address_line2" fullWidth label="address_line2" />
      <TextInput source="city" fullWidth label="city" />
      <TextInput source="state" fullWidth label="state" />
      <TextInput source="postal_code" fullWidth label="postal_code" />
      <TextInput source="country" fullWidth label="country" />
    </SimpleForm>
  </Create>
);
