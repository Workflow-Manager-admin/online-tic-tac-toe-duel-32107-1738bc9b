interface GameUser {
  user_id: string
  name: string
  is_guest?: boolean
}
interface Game {
  game_id: string
  player_x: GameUser | null
  player_o: GameUser | null
  board: (string | null)[][]
  turn: string
  status: 'waiting' | 'active' | 'done'
  winner: string | null
  draw?: boolean
}
type GameHandler = (gameData: Game) => void
type StatusHandler = (status: string) => void

/**
 * PUBLIC_INTERFACE
 * Connects to backend websocket for real-time game updates.
 * @param gameId 
 * @param token 
 * @param onMessage (handles game updates)
 * @param onStatus (handles connection status)
 */
export function connectGameWebSocket(
  gameId: string,
  token: string,
  onMessage: GameHandler,
  onStatus?: StatusHandler
): WebSocket {
  const wsProto = location.protocol.startsWith('https') ? 'wss' : 'ws'
  const url = `${wsProto}://${location.hostname}:3001/ws/game/${gameId}?token=${encodeURIComponent(token)}`
  const ws = new WebSocket(url)
  ws.onopen = () => { if (onStatus) onStatus('WebSocket Connected') }
  ws.onerror = () => { if (onStatus) onStatus('WebSocket error') }
  ws.onclose = () => { if (onStatus) onStatus('WebSocket closed') }
  ws.onmessage = (ev) => {
    try {
      const msg = JSON.parse(ev.data)
      if ('game' in msg) {
        onMessage(msg.game as Game)
      }
    } catch {
      // ignore
    }
  }
  return ws
}
