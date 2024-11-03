"use client";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    label: string;
}

const Button: React.FC<ButtonProps> = ({ label, className, ...props }) => {
    return (
        <button
            className={`bg-primary text-white py-2 px-4 rounded hover:bg-accent ${className}`}
            {...props}
        >
            {label}
        </button>
    );
};
export default Button;