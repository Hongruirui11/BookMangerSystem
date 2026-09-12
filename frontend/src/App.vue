<script setup>
import { computed, onMounted, ref } from 'vue'

const books = ref([])
const keyword = ref('')
const loading = ref(false)
const error = ref('')
const filteredBooks = computed(() => {
  const text = keyword.value.trim().toLowerCase()
  if (!text) return books.value
  return books.value.filter((book) => `${book.title}${book.author}`.toLowerCase().includes(text))
})

async function loadBooks() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch('http://127.0.0.1:8000/api/books/')
    if (!response.ok) throw new Error('图书列表加载失败')
    books.value = (await response.json()).items
  } catch (err) {
    error.value = `${err.message}。请确认 FastAPI 已启动。`
  } finally { loading.value = false }
}

onMounted(loadBooks)
</script>

<template>
  <div class="app-shell">
    <header class="topbar"><span class="mark">书架 / 01</span><span class="status">TEACHING EDITION</span></header>
    <main>
      <section class="intro">
        <p class="kicker">A SMALL LIBRARY, CLEARLY ARRANGED</p>
        <h1>给每一本书<br /><em>一个位置。</em></h1>
        <p class="description">一个用 Vue 和 FastAPI 写成的学习项目。先从目录开始，再逐步连接数据库。</p>
      </section>
      <section class="toolbar">
        <label for="search">检索目录</label>
        <input id="search" v-model="keyword" placeholder="输入书名或作者…" />
        <button type="button" @click="loadBooks">刷新</button>
      </section>
      <p v-if="loading" class="notice">正在翻开目录…</p>
      <p v-else-if="error" class="notice error">{{ error }}</p>
      <section v-else class="book-grid">
        <article v-for="(book, index) in filteredBooks" :key="book.id" class="book-card">
          <span class="index">{{ String(index + 1).padStart(2, '0') }}</span>
          <h2>{{ book.title }}</h2><p>{{ book.author }}</p>
          <span class="arrow">↗</span>
        </article>
        <p v-if="!filteredBooks.length" class="notice">没有找到匹配的书。试试另一个关键词。</p>
      </section>
    </main>
    <footer><span>Vue 3 × FastAPI</span><span>API /api/books</span></footer>
  </div>
</template>

