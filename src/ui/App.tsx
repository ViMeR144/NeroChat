import { useEffect, useState } from 'react'
import { Chat } from './Chat'
import { Auth } from './Auth'
import { getToken } from '../utils/auth'

export function App() {
	const [dark, setDark] = useState(true)
	const [authed, setAuthed] = useState<boolean>(!!getToken())

	useEffect(() => {
		document.body.className = dark ? 'theme-dark' : 'theme-light'
	}, [dark])

	return (
		<div className={dark ? 'theme-dark' : 'theme-light'}>
			<header className="app-header">
				<div className="brand">NeoChat</div>
				<div className="actions">
					<button onClick={() => setDark(d => !d)}>{dark ? '🌙' : '☀️'}</button>
				</div>
			</header>
			<main className="app-main">
				{authed ? <Chat /> : <Auth onDone={() => setAuthed(true)} />}
			</main>
			<footer className="app-footer">RU/EN • Math tool • Powered by your LLM</footer>
		</div>
	)
}

