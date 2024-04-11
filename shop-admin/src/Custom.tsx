import React from "react";
import { Edit, SimpleForm, TextInput, SelectInput } from "react-admin";

interface CustomEditProps {
  id: string;
  // status: string;

  // دیگر فیلدها
}

const CustomEdit: React.FC<CustomEditProps> = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <SelectInput
        source="status"
        choices={[
          { id: "Confirmation", name: "Confirmation" },
          { id: "Send", name: "Send" },
          { id: "Delivery", name: "Delivery" },
          { id: "Cancel", name: "Cancel" },
        ]}
      />
    </SimpleForm>
  </Edit>
);

const CustomEditGuesser: React.FC<CustomEditProps> = (props) => (
  <CustomEdit {...props} />
);

export default CustomEditGuesser;
