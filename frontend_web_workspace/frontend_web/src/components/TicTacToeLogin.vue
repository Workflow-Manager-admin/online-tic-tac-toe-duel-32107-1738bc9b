<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import { guestLogin } from '../composables/useApi'

const emit = defineEmits(['login-success'])

const name = ref('')
const loading = ref(false)
const error = ref('')

interface LoginResponse {
  user: { user_id: string, name: string, is_guest: boolean }
  token: string
}

// Attempt guest login and emit result to parent
async function loginHandler() {
  if (!name.value) {
    error.value = 'Name is required.'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const result = await guestLogin(name.value)
    emit('login-success', result as LoginResponse)
  } catch {
    error.value = 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-wrapper">
    <h2>Tic Tac Toe</h2>
    <input
      v-model="name"
      @keyup.enter="loginHandler"
      :disabled="loading"
      placeholder="Enter your name to play as guest"
      autocomplete="off"
      autofocus
    />
    <button :disabled="loading || !name" @click="loginHandler">Enter as Guest</button>
    <div class="error" v-if="error">{{ error }}</div>
  </div>
</template>

<style scoped>
.login-wrapper {
  max-width: 320px;
  margin: 140px auto 0 auto;
  padding: 2rem 1.5rem 2.5rem 1.5rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 18px 0 rgba(27,43,77,0.04);
  text-align: center;
}
h2 {
  color: #1976d2;
  margin-bottom: 1.5rem;
}
input {
  width: 90%;
  padding: 0.7rem;
  border: 1px solid #1976d2;
  border-radius: 6px;
  margin: .3rem 0 1rem 0;
  font-size: 1.08rem;
}
button {
  background: #1976d2;
  color: #fff;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  padding: 0.65rem 1.7rem;
  font-size: 1.03rem;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: background .2s;
}
button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
.error {
  color: #c00;
  font-size: 0.97em;
  margin-top: 1rem;
}
</style>
