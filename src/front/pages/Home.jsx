import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";


const Comment = ({ comment }) => (
	<div className="card mb-2">
		<div className="card-body">
			<h6 className="card-subtitle mb-2 text-muted">{comment.author.email}</h6>
			<p className="card-text">{comment.comment_text}</p>
		</div>
	</div>
);

const Post = ({ post }) => (
	<div className="card mb-3">
		<div className="card-body">
			<h5 className="card-title">{post.user.email}</h5>
			<p className="card-text">{post.content}</p>
			{
				post.comments && post.comments.length > 0 ? (
					<div className="mt-3">
						<h6>Comments:</h6>
						{post.comments.map((comment) => (
							<Comment key={comment.id} comment={comment} />
						))}
					</div>
				) : (
					<p className="text-muted">No comments yet.</p>
				)
			}
		</div>
	</div>
);


export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	const loadFeed = async () => {
		try {
			const backendUrl = import.meta.env.VITE_BACKEND_URL

			if (!backendUrl) throw new Error("VITE_BACKEND_URL is not defined in .env file")

			const response = await fetch(backendUrl + "/api/post")
			const data = await response.json()

			if (response.ok) dispatch({ type: "update_posts", payload: data })
			return data

		} catch (error) {
			if (error.message) throw new Error(
				`Could not fetch the posts from the backend.`
			);
		}

	}

	useEffect(() => {
		loadFeed()
	}, [])

	return (
		<div className="text-center mt-5">
			<h1 className="display-4">Unsocial Network Data Model</h1>

			{
				store.posts.length > 0 ? (
					store.posts.map((post) => (
						<Post key={post.id} post={post} />
					))
				) : (
					<p>No posts available.</p>
				)
			}
		</div>
	);
}; 