import LoginPage from "../components/LoginPage.jsx";

export default {
    title: 'Login',
    component: LoginPage,
};

const Template = (args) => <LoginPage {...args} />;

export const Default = Template.bind({});

Default.args = {
    
};