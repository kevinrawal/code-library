import { BrowserRouter } from 'react-router-dom';
import LoginPage from "../components/auth/LoginPage.jsx";
import "../index.css"

export default {
    title: 'Login',
    component: LoginPage,
    decorators: [
    (Story) => (
      <BrowserRouter>
        <Story />
      </BrowserRouter>
    ),
  ],
};

const Template = (args) => <LoginPage {...args} />;

export const Default = Template.bind({});

Default.args = {};