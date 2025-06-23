import axios from 'axios'

const API_BASE = import.meta.env.VITE_TTT_BACKEND_URL || 'http://localhost:3001'

// PUBLIC_INTERFACE
export async function guestLogin(name: string) {
  const resp = await axios.post(`${API_BASE}/api/auth/guest`, { name })
  return resp.data
}

// PUBLIC_INTERFACE
export async function listWaitingGames() {
  const resp = await axios.get(`${API_BASE}/api/game/list`)
  return resp.data
}

// PUBLIC_INTERFACE
export async function createGame(user_id: string) {
  const resp = await axios.post(`${API_BASE}/api/game/create`, { user_id })
  return resp.data
}

// PUBLIC_INTERFACE
export async function joinGame(user_id: string, game_id: string) {
  const resp = await axios.post(`${API_BASE}/api/game/join`, { user_id, game_id })
  return resp.data
}

// PUBLIC_INTERFACE
export async function submitMove(user_id: string, row: number, col: number, game_id: string) {
  const resp = await axios.post(`${API_BASE}/api/game/move`, {
    user_id, row, col, game_id
  })
  return resp.data
}

// PUBLIC_INTERFACE
export async function getGameState(game_id: string) {
  const resp = await axios.get(`${API_BASE}/api/game/${game_id}`)
  return resp.data
}
