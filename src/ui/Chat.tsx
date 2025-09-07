import { useMemo, useRef, useState } from 'react'
import { apiChat } from '../utils/api'

export type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string }

export function Chat() {
	const [messages, setMessages] = useState<ChatMessage[]>([])
	const [input, setInput] = useState('')
	const [loading, setLoading] = useState(false)
	const listRef = useRef<HTMLDivElement>(null)

	const canSend = input.trim().length > 0 && !loading

	const handleSend = async () => {
		if (!canSend) return
		const userMsg: ChatMessage = { role: 'user', content: input.trim() }
		setMessages(prev => [...prev, userMsg])
		setInput('')
		setLoading(true)
		try {
			const answer = await apiChat([...messages, userMsg])
			setMessages(prev => [...prev, { role: 'assistant', content: answer }])
		} catch (e: any) {
			const detail = e?.message || 'Ошибка запроса. Попробуйте позже.'
			setMessages(prev => [...prev, { role: 'assistant', content: detail }])
		} finally {
			setLoading(false)
			setTimeout(() => listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' }), 50)
		}
	}

	const placeholder = useMemo(() => 'Спросите что угодно… Ask anything…', [])

	return (
		<div className="chat">
			<div className="messages" ref={listRef}>
				{messages.length === 0 && (
					<div className="empty">
						<h2>Добро пожаловать в NeoChat</h2>
						<p>RU/EN ответы, объяснения решений и примеров. Введите вопрос ниже.</p>
					</div>
				)}
				{messages.map((m, i) => (
					<div key={i} className={`msg ${m.role}`}>
						<div className="avatar">{m.role === 'user' ? '🧑' : '🤖'}</div>
						<div className="bubble">{m.content}</div>
					</div>
				))}
				{loading && (
					<div className="msg assistant">
						<div className="avatar">🤖</div>
						<div className="bubble">
							<div className="typing"><span></span><span></span><span></span></div>
						</div>
					</div>
				)}
			</div>
			<div className="composer">
				<input
					type="text"
					value={input}
					placeholder={placeholder}
					onChange={e => setInput(e.target.value)}
					onKeyDown={e => {
						if (e.key === 'Enter' && !e.shiftKey) {
							e.preventDefault()
							handleSend()
						}
					}}
				/>
				<button onClick={handleSend} disabled={!canSend}>{loading ? '...' : 'Отправить'}</button>
			</div>
		</div>
	)
}

