import { Link } from "react-router-dom";

export const Navbar = () => {

	return (
		<nav className="navbar navbar-dark bg-dark">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">UN</span>
				</Link>
				<div className="ml-auto">
					<Link to="/register">
						<button className="btn btn-primary">Register</button>
					</Link>
					<Link to="/login" className="ms-2">
						<button className="btn btn-secondary">Login</button>
					</Link>
				</div>
			</div>
		</nav>
	);
};