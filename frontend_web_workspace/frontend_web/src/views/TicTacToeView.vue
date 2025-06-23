<script setup lang="ts">
import { ref } from 'vue'
import TicTacToeLogin from '../components/TicTacToeLogin.vue'
import TicTacToeLobby from '../components/TicTacToeLobby.vue'
import TicTacToeBoard from '../components/TicTacToeBoard.vue'

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

const loginSuccess = ref(false)
const user = ref<GameUser|null>(null)
const token = ref('')
const game = ref<Game|null>(null)

function handleLogin({ user: sessionUser, token: t }: { user: GameUser, token: string }) {
  user.value = sessionUser
  token.value = t
  loginSuccess.value = true
}

function handleEnterGame(newGame: Game) {
  game.value = newGame
}
function handleGameUpdated(updatedGame: Game) {
  game.value = updatedGame
}
</script>

<template>
  <div>
    <TicTacToeLogin v-if="!loginSuccess" @login-success="handleLogin" />
    <TicTacToeLobby
      v-else-if="!game && user"
      :user="user"
      @enter-game="handleEnterGame"
    />
    <TicTacToeBoard
      v-else-if="game && user"
      :user="user"
      :token="token"
      :game="game"
      @game-updated="handleGameUpdated"
    />
  </div>
</template>
