<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed, onUnmounted } from 'vue'
import { submitMove } from '../composables/useApi'
import { connectGameWebSocket } from '../composables/useWebSocket'

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

const props = defineProps<{
  game: Game,
  user: GameUser,
  token: string
}>()
const emit = defineEmits<{
  (e: 'game-updated', game: Game): void
}>()

const wsRef = ref<WebSocket|null>(null)
const internalGame = ref<Game>({...props.game})
const moveError = ref('')
const wsStatus = ref('')

const userMark = computed(() =>
  internalGame.value.player_x?.user_id === props.user.user_id
    ? 'X'
    : internalGame.value.player_o?.user_id === props.user.user_id
      ? 'O'
      : null
)

function renderCellLabel(i: number, j: number) {
  return internalGame.value.board[i][j] || ''
}

async function handleMove(row:number, col:number) {
  moveError.value = ''
  if (internalGame.value.status !== 'active') return
  if (internalGame.value.turn !== userMark.value) {
    moveError.value = "It's not your turn."
    return
  }
  if (internalGame.value.board[row][col]) {
    moveError.value = "Cell occupied."
    return
  }
  try {
    const game = await submitMove(props.user.user_id, row, col, internalGame.value.game_id)
    emit('game-updated', game as Game)
    internalGame.value = { ...(game as Game) }
  } catch {
    moveError.value = 'Invalid move or error.'
  }
}

// Handle real-time updates
const onMessage = (game: Game) => {
  internalGame.value = { ...game }
  emit('game-updated', game)
}

const onWsStatus = (status: string) => {
  wsStatus.value = status
}

// Set up websocket on mount and watch for game_id changes
function setupWebSocket() {
  if (wsRef.value) wsRef.value.close()
  wsRef.value = connectGameWebSocket(internalGame.value.game_id, props.token, onMessage, onWsStatus)
}
watch(() => props.game.game_id, () => setupWebSocket(), { immediate: true })
onUnmounted(() => { if (wsRef.value) wsRef.value.close() })

function cellDisabled(i:number, j:number) {
  return !!internalGame.value.board[i][j] ||
    internalGame.value.status !== "active" ||
    internalGame.value.turn !== userMark.value
}

const winnerLabel = computed(() => {
  return internalGame.value.status === 'done'
    ? (internalGame.value.winner
        ? `${internalGame.value.winner === userMark.value ? "You win!" : "You lose!"}`
        : (internalGame.value.draw ? "Draw!" : "Opponent wins!"))
    : ''
});
</script>

<template>
  <div class="ttt-main">
    <div class="status-bar">
      <div>{{ internalGame.status === 'done' ? 'Game Over' : internalGame.status === 'waiting' ? 'Waiting for Player' : 'In Progress' }}</div>
      <div class="turn-label" v-if="internalGame.status==='active'">
        Your mark: <span class="pill" :class="userMark">{{ userMark }}</span> •
        <span v-if="internalGame.turn === userMark">Your turn!</span>
        <span v-else>Opponent's turn</span>
      </div>
      <div class="winner-label" v-if="internalGame.status==='done'">
        {{ winnerLabel }}
      </div>
    </div>
    <div class="board-wrap">
      <div class="game-board">
        <div v-for="i in 3" :key="i" class="board-row">
          <button
            v-for="j in 3"
            :key="j"
            class="cell"
            :class="{ accent: internalGame.board[i-1][j-1]==='X', secondary: internalGame.board[i-1][j-1]==='O' }"
            :disabled="cellDisabled(i-1, j-1)"
            @click="handleMove(i-1, j-1)"
          >
            {{ renderCellLabel(i-1, j-1) }}
          </button>
        </div>
      </div>
      <div class="move-history">
        <h4>Move History</h4>
        <ul>
          <li v-for="(row, rIdx) in internalGame.board" :key="`mr${rIdx}`">
            <span v-for="(cell, cIdx) in row" :key="`mc${rIdx}-${cIdx}`">
              <span v-if="cell">{{ cell }}</span>
              <span v-else>&nbsp;</span>
            </span>
          </li>
        </ul>
      </div>
    </div>
    <div class="move-error" v-if="moveError">{{ moveError }}</div>
    <div class="ws-status" v-if="wsStatus">{{ wsStatus }}</div>
  </div>
</template>

<style scoped>
.ttt-main {
  margin: 50px auto 0 auto;
  padding: 2rem 0 2rem 0;
  max-width: 700px;
}
.status-bar {
  color: #1976d2;
  text-align: center;
  margin-bottom: 1.6rem;
  font-size: 1.15rem;
  font-weight: 600;
  border-bottom: 1.5px solid #e0e0e0;
  padding-bottom: 12px;
}
.turn-label, .winner-label {
  margin-top: 5px;
  font-size:1.06em;
  color: #424242;
}
.pill {
  display: inline-block;
  min-width: 30px;
  padding: 3px 12px;
  border-radius: 14px;
  margin-left: 7px;
  color: #fff;
  font-weight: 600;
}
.pill.X { background: #1976d2; }
.pill.O { background: #424242; }

.board-wrap {
  margin: 0 auto;
  display: flex;
  flex-direction: row;
  justify-content: center;
}
.game-board {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-right: 2.3rem;
  flex-shrink:0;
}
.board-row {
  display: flex;
  flex-direction: row;
}
.cell {
  width: 70px;
  height: 70px;
  margin: 4px;
  border: 2.5px solid #1976d2;
  border-radius: 11px;
  background: #fff;
  font-size: 2.65rem;
  color: #1976d2;
  font-weight:bold;
  text-align: center;
  transition: background .23s;
  cursor: pointer;
}
.cell:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
  color: #bbb;
  border-color: #dadada;
}
.cell.accent { color: #1976d2; background: #ffeb3b25; }
.cell.secondary { color: #fff; background: #424242; }
.move-history {
  background: #fafafb;
  border-radius: 10px;
  padding: 18px 10px 8px 20px;
  min-width: 180px;
  margin-left: 1.5rem;
  box-shadow: 0 1px 5px 0 rgba(27,43,77,0.06);
}
.move-history h4 {
  font-size: 1.08rem;
  color: #424242;
  font-weight: bold;
  margin-bottom: 10px;
}
.move-history ul {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 1.17em;
  letter-spacing: 0.2em;
}
.move-history li {
  margin-bottom: 2px;
}
.move-error {
  color: #c00;
  text-align:center;
  margin-top: .8rem;
}
.ws-status {
  color: #ffab00;
  text-align:center;
  margin-top: .7rem;
  font-size: 0.99em;
}
</style>
