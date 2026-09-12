<script setup>
import { computed, onMounted, ref } from 'vue'

const books = ref([])
const keyword = ref('')
const loading = ref(false)
const error = ref('')
const showForm = ref(false)
const editingId = ref(null)
const detailBook = ref(null)
const form = ref({ title: '', author: '', isbn: '', publisher: '', published_year: '', description: '' })
const filteredBooks = computed(() => books.value)

async function loadBooks() {
  loading.value = true
  error.value = ''
  try {
    const path = keyword.value.trim()
      ? `/api/books/search?keyword=${encodeURIComponent(keyword.value.trim())}`
      : '/api/books/'
    const response = await fetch(`http://127.0.0.1:8000${path}`)
    if (!response.ok) throw new Error('图书列表加载失败')
    books.value = (await response.json()).items
  } catch (err) {
    error.value = `${err.message}。请确认 FastAPI 已启动。`
  } finally { loading.value = false }
}

function resetForm() {
  form.value = { title: '', author: '', isbn: '', publisher: '', published_year: '', description: '' }
  editingId.value = null
}

function startCreate() {
  resetForm()
  showForm.value = true
  detailBook.value = null
}

function startEdit(book) {
  editingId.value = book.id
  form.value = { ...book }
  showForm.value = true
  detailBook.value = null
}

async function saveBook() {
  error.value = ''
  try {
    const isEdit = editingId.value !== null
    const response = await fetch(`http://127.0.0.1:8000/api/books/${isEdit ? editingId.value : ''}`, {
      method: isEdit ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (!response.ok) throw new Error('保存失败，请检查表单内容')
    resetForm()
    showForm.value = false
    await loadBooks()
  } catch (err) { error.value = err.message }
}

async function removeBook(book) {
  if (!window.confirm(`确定删除《${book.title}》吗？`)) return
  const response = await fetch(`http://127.0.0.1:8000/api/books/${book.id}`, { method: 'DELETE' })
  if (!response.ok) { error.value = '删除失败'; return }
  detailBook.value = null
  await loadBooks()
}

function showDetail(book) {
  detailBook.value = detailBook.value?.id === book.id ? null : book
  showForm.value = false
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
        <button type="button" @click="showForm ? (showForm = false) : startCreate()">{{ showForm ? '关闭表单' : '新增图书' }}</button>
        <button type="button" @click="loadBooks">{{ keyword ? '执行搜索' : '刷新' }}</button>
      </section>
      <form v-if="showForm" class="book-form" @submit.prevent="saveBook">
        <p class="form-title">{{ editingId ? '编辑图书' : '新增图书' }}</p>
        <input v-model="form.title" required placeholder="书名" />
        <input v-model="form.author" required placeholder="作者" />
        <input v-model="form.publisher" placeholder="出版社（可选）" />
        <input v-model="form.isbn" placeholder="ISBN（可选）" />
        <input v-model="form.published_year" type="number" placeholder="出版年份（可选）" />
        <button type="submit">{{ editingId ? '保存修改' : '保存图书' }}</button>
      </form>
      <aside v-if="detailBook" class="detail-panel">
        <span class="eyebrow">BOOK DETAIL / {{ detailBook.id }}</span>
        <h2>{{ detailBook.title }}</h2><p>{{ detailBook.author }}</p>
        <p>{{ detailBook.publisher || '未填写出版社' }} · {{ detailBook.published_year || '年份未知' }}</p>
        <button type="button" @click="startEdit(detailBook)">编辑</button>
        <button type="button" class="danger" @click="removeBook(detailBook)">删除</button>
      </aside>
      <p v-if="loading" class="notice">正在翻开目录…</p>
      <p v-else-if="error" class="notice error">{{ error }}</p>
      <section v-else class="book-grid">
        <article v-for="(book, index) in filteredBooks" :key="book.id" class="book-card">
          <span class="index">{{ String(index + 1).padStart(2, '0') }}</span>
          <button class="book-hit-area" type="button" @click="showDetail(book)">
            <h2>{{ book.title }}</h2><p>{{ book.author }}</p><span class="arrow">↗</span>
          </button>
        </article>
        <p v-if="!filteredBooks.length" class="notice">没有找到匹配的书。试试另一个关键词。</p>
      </section>
    </main>
    <footer><span>Vue 3 × FastAPI</span><span>API /api/books</span></footer>
  </div>
</template>
