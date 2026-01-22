import { useState } from "react";
import { FormField } from "./Register";


const Login = () => {

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

    const [userCredentials, setUserCredentials] = useState({
        email: "",
        password: ""
    });

    const handleFieldChange = (e) => {
        setUserCredentials({
            ...userCredentials,
            [e.target.name]: e.target.value
        });
    }

    const submitLoginForm = async (e) => {
        e.preventDefault();

        const resp = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userCredentials)
        });

        if (resp.ok) {
            const data = await resp.json();
            alert("Login successful! Token: " + data.access_token);
        }

    }

    return (

        <div className="container mt-5">
            <h2>Login Page</h2>
            <form onSubmit={submitLoginForm}>
                <div className="mb-3">
                    {
                        fields.map((field, index) => (
                            <FormField key={index} field={field} onChange={handleFieldChange} />
                        ))
                    }
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
        </div>

    )
};

export default Login;