import type { ChatMessage } from '../ui/Chat'
import { getToken } from './auth'

const BASE = (import.meta.env.VITE_API_BASE as string) || ''

export async function apiChat(messages: ChatMessage[]): Promise<string> {
	const headers: Record<string, string> = { 'Content-Type': 'application/json' }
	const token = getToken()
	if (token) headers['Authorization'] = `Bearer ${token}`
	const res = await fetch(`${BASE}/api/chat`, {
		method: 'POST',
		headers,
		body: JSON.stringify({ messages, use_math_tool: true })
	})
	if (!res.ok) {
		let detail = 'Request failed'
		try {
			const data = await res.json()
			detail = data?.detail ?? JSON.stringify(data)
		} catch {
			try { detail = await res.text() } catch {}
		}
		throw new Error(detail)
	}
	const data = await res.json()
	return data.answer as string
}
