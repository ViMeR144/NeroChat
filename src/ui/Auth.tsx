import { useState } from 'react'
import { apiLogin, apiRegister, saveToken } from '../utils/auth'

export function Auth({ onDone }: { onDone: () => void }) {
	const [isLogin, setIsLogin] = useState(true)
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	function validate(): string | null {
		const emailOk = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)
		if (!emailOk) return 'Введите корректный email (например, user@example.com)'
		if (password.length < 4) return 'Пароль должен быть не короче 4 символов'
		return null
	}

	async function submit() {
		const v = validate()
		if (v) { setError(v); return }
		setLoading(true)
		setError(null)
		try {
			const token = isLogin ? await apiLogin(email, password) : await apiRegister(email, password)
			saveToken(token)
			onDone()
		} catch (e: any) {
			let msg = e?.message || 'Ошибка'
			try {
				const parsed = JSON.parse(msg)
				if (parsed?.detail) {
					if (typeof parsed.detail === 'string') msg = parsed.detail
					else if (Array.isArray(parsed.detail) && parsed.detail[0]?.msg) msg = parsed.detail[0].msg
				}
			} catch {}
			setError(msg)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="auth-panel">
			<h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
			<input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
			<input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Пароль" />
			{error && <div className="error">{error}</div>}
			<button onClick={submit} disabled={loading}>{loading ? '...' : (isLogin ? 'Войти' : 'Создать аккаунт')}</button>
			<div className="switch" onClick={() => setIsLogin(v => !v)}>
				{isLogin ? 'Нет аккаунта? Регистрация' : 'Уже есть аккаунт? Войти'}
			</div>
		</div>
	)
}
