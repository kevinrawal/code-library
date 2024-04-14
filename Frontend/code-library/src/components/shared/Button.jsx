import React from "react";

const Button = ({ title, type = "default", size = "md", onClickFunction }) => {
  // Define default colors based on type
  const themeClasses = {
    default: {
      bg: "indigo-500",
      hover: "indigo-700",
      text: "white",
    },
    danger: {
      bg: "red-500",
      hover: "red-700",
      text: "white",
    },
  };

  // Apply Tailwind CSS classes based on size
  const sizeClasses = {
    sm: "px-2 py-1",
    md: "px-4 py-2",
    lg: "px-6 py-3",
  };

  const handleClick = () => {
    if (onClickFunction) {
      onClickFunction();
    }
  };

  return (
    <button
      type="button"
      className={`inline-flex items-center ${sizeClasses[size]} bg-${themeClasses[type].bg} hover:bg-${themeClasses[type].hover} text-${themeClasses[type].text} font-bold rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700`}
      onClick={() => handleClick()}
    >
      {title}
    </button>
  );
};

export default Button;
