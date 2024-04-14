import React from "react";
import Button from "../../components/shared/Button.jsx";

export default {
  title: "shared/Button",
  component: Button,
  argTypes: {
    type: {
      control: {
        type: "select",
        options: ["default", "danger"],
      },
    },
  },
};

export const Default = (args) => <Button {...args} />;
Default.args = {
  title: "Default",
  type: "default",
};

export const Danger = (args) => <Button {...args} />;
Danger.args = {
  title: "Danger",
  type: "danger",
};

export const AllButtons = () => (
  <div>
    <Default title="Default" type="default" />
    <Danger title="Danger" type="danger" />
  </div>
);