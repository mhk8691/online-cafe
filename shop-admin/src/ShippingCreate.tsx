import * as React from "react";
import {
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  required,
  NumberInput,
  SelectInput,
} from "react-admin";

export const ShippingCreate = () => (
  <Create>
    <SimpleForm>
      <SelectInput // Use SelectInput for category selection if applicable
        source="customer_id"
        label="customer_id"
        fullWidth
        choices={[
          // Replace with your category options
          { id: 8, name: "customer 1" },
          { id: 9, name: "customer 2" },
          { id: 18, name: "customer 3" },
          { id: 20, name: "customer 4" },
        ]}
      />
      <TextInput source="recipient_name" label="recipient_name" fullWidth />
      <TextInput source="address_line1" fullWidth label="address_line1" />
      <TextInput source="address_line2" fullWidth label="address_line2" />
      <TextInput source="city" fullWidth label="city" />
      <TextInput source="state" fullWidth label="state" />
      <TextInput source="postal_code" fullWidth label="postal_code" />
      <TextInput source="country" fullWidth label="country" />
    </SimpleForm>
  </Create>
);
