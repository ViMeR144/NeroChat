export type AuthToken = string;

const TOKEN_KEY = 'neochat_token';

export function saveToken(token: AuthToken) {
	localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): AuthToken | null {
	return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
	localStorage.removeItem(TOKEN_KEY);
}

export async function apiRegister(email: string, password: string): Promise<AuthToken> {
	const res = await fetch('/api/auth/register', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});
	if (!res.ok) throw new Error(await res.text());
	const data = await res.json();
	return data.token as string;
}

export async function apiLogin(email: string, password: string): Promise<AuthToken> {
	const res = await fetch('/api/auth/login', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});
	if (!res.ok) throw new Error(await res.text());
	const data = await res.json();
	return data.token as string;
}
