<script setup lang="ts">
import { ref, defineProps, defineEmits, onMounted } from 'vue'
import { listWaitingGames, createGame, joinGame } from '../composables/useApi'

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
  user: GameUser
}>()

const emit = defineEmits<{
  (e: 'enter-game', game: Game): void
}>()

const waitingGames = ref<Game[]>([])
const loading = ref(true)
const joinError = ref('')
const createLoading = ref(false)

async function refreshGames() {
  loading.value = true
  waitingGames.value = []
  try {
    waitingGames.value = await listWaitingGames() as Game[]
  } catch {
    // ignore for now
  }
  loading.value = false
}

// Start a new game and enter
async function startGame() {
  createLoading.value = true
  try {
    const game = await createGame(props.user.user_id)
    emit('enter-game', game as Game)
  } finally {
    createLoading.value = false
  }
}

// Join an available waiting game
async function joinGameHandler(game_id: string) {
  joinError.value = ''
  try {
    const game = await joinGame(props.user.user_id, game_id)
    emit('enter-game', game as Game)
  } catch {
    joinError.value = 'Unable to join game.'
  }
}

onMounted(() => {
  refreshGames()
})
</script>

<template>
  <div class="lobby-wrapper">
    <h2>Welcome, {{ user.name }}</h2>
    <button :disabled="createLoading" class="primary" @click="startGame">
      Start New Game
    </button>
    <div class="games-list">
      <h3>Join a Waiting Game</h3>
      <p v-if="loading">Fetching games...</p>
      <ul v-else>
        <li v-for="game in waitingGames" :key="game.game_id">
          <span>{{ game.player_x?.name || 'Waiting Player' }}</span>
          <button class="accent" @click="joinGameHandler(game.game_id)">
            Join
          </button>
        </li>
        <li v-if="!waitingGames.length && !loading">No games available.</li>
      </ul>
    </div>
    <div class="error" v-if="joinError">{{ joinError }}</div>
  </div>
</template>

<style scoped>
.lobby-wrapper {
  max-width: 410px;
  margin: 70px auto 0 auto;
  padding: 2rem 1.5rem 2.2rem 1.5rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 18px 0 rgba(27,43,77,0.04);
  text-align: center;
}
h2 {
  color: #1976d2;
  margin-bottom: 1.2rem;
  font-weight: bold;
}
.games-list {
  margin: 2.5rem 0 .2rem 0;
  text-align:left;
}
h3 {
  color: #424242;
  font-size: 1.18rem;
  text-align:left;
  margin-bottom: .5rem;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  background: #f8f8f8;
  display: flex;
  align-items:center;
  justify-content: space-between;
  margin-bottom: 9px;
  padding: 0.68rem 0.7rem;
  border-radius: 0.47rem;
}
.primary {
  background: #1976d2;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  padding: 0.65rem 1.7rem;
  font-size: 1.03rem;
  letter-spacing: 0.04em;
  cursor: pointer;
  margin-bottom: 1.2rem;
  margin-top:0.3rem;
}
.accent {
  background: #ffeb3b;
  color: #222;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  padding: 0.42rem 0.97rem;
  margin-left: 0.1rem;
  cursor: pointer;
}
.error {
  color: #c00;
  font-size: 0.98em;
  margin-top: 1rem;
  text-align: left;
}
</style>
