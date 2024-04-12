import React from "react";
import { Edit, SimpleForm, TextInput, SelectInput } from "react-admin";

interface CustomEditProps {
  id: string;
  // status: string;

  // دیگر فیلدها
}

const UserEdit: React.FC<CustomEditProps> = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="username"  fullWidth />

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
          { id: "RegularAdmin", name: "RegularAdmin" },
        ]}
      />
    </SimpleForm>
  </Edit>
);

const CustomEditGuesser: React.FC<CustomEditProps> = (props) => (
  <UserEdit {...props} />
);

export default CustomEditGuesser;
