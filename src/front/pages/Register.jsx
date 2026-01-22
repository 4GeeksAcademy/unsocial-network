import { useState } from "react";

export const FormField = ({ field, onChange }) => (
    <div className="mb-3">
        <label htmlFor={field.name} className="form-label">{field.label}</label>
        <input type={field.name === 'password' ? 'password' : 'text'} className="form-control"
            id={field.name} name={field.name} placeholder={field.placeholder}
            onChange={onChange}
        />
    </div>
);

const Register = () => {

    const fields = [
        {
            name: "email",
            label: "Email address",
            placeholder: "Enter your email"
        },
        {
            name: "password",
            label: "Password",
            placeholder: "Enter your password"
        }
    ];

    const [newUser, setNewUser] = useState({
        email: "",
        password: ""
    });

    const handleRegisterForm = async (e) => {
        e.preventDefault();
 
        const resp = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ...newUser,
                is_active: true
            })
        });

        if (resp.ok) {
            alert("User registered successfully!");
        }
        return false;
    }

    const changeField = (e) => {
        setNewUser({
            ...newUser,
            [e.target.name]: e.target.value
        });
    }

    return (
        <div className="container mt-5">
            <h2>Register New User</h2>
            <form onSubmit={handleRegisterForm}>
                <div className="mb-3">
                    {
                        fields.map((field, index) => (
                            <FormField key={index} field={field} onChange={changeField} />
                        ))
                    }
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>

        </div>
    );
}

export default Register;