<template lang="pug">
BContainer.py-4.body
  BCard.shadow-sm.border-0
    BCardBody.p-4
      .d-flex.flex-column.flex-md-row.align-items-md-center.justify-content-between.gap-3.mb-4
        h1.h3.mb-0 📝 Мои заметки
        BBadge.bg-primary.rounded-pill.fs-6(v-if="!loading") {{ notes.length }} заметок

      BAlert(
        v-if="statusMessage"
        :variant="statusType === 'success' ? 'success' : 'danger'"
        show
      ) {{ statusMessage }}

      //- Поле поиска
      BFormGroup.mb-4(label="Поиск по заметкам")
        BFormInput(
          v-model="searchQuery"
          @input="handleSearch"
          placeholder="Введите текст для поиска..."
          type="search"
        )

      BForm(@submit.prevent="createNote")
        BFormGroup.mb-3(label="Новая заметка" label-for="new-note-text")
          QuillEditor(
            theme="snow"
            v-model:content="newNoteText"
            contentType="html"
            :toolbar="toolbarOptions"
            placeholder="Напишите новую заметку..."
          )

        .d-flex.justify-content-end
          BButton(variant="primary" type="submit" :disabled="loading") ➕ Добавить

      .text-center.py-5(v-if="loading")
        BSpinner(variant="primary" label="Загрузка заметок")
        .mt-2 Загрузка заметок...

      .text-center.py-5(v-else-if="notes.length === 0")
        .display-6 🎉
        p.mb-0 У вас еще нет заметок

      BRow.g-3.mt-4.p-4(v-else)
        BCol(cols="12" md="6" lg="4" v-for="note in notes" :key="note.id")
          BCard(border-variant="primary" align="center" card-height="100%" class="h-100")
            BCardTitle
              .small.text-muted.mb-2 📅 {{ formatDate(note.created_at) }}
              .small.text-muted(v-if="note.updated_at !== note.created_at") ✏️ {{ formatDate(note.updated_at) }}
            BCardText
              .ql-snow
                .ql-editor(v-html="note.text" contenteditable="true" style="padding: 0;")

            template.d-flex.gap-2(#footer)
              BButton(variant="outline-primary" size="sm" @click="editNote(note)") Изменить
              BButton(variant="outline-danger" size="sm" @click="deleteNote(note.id)") Удалить

  BModal(v-model="isEditModalOpen" title="Редактирование заметки" centered)
    BFormGroup(label="Текст заметки")
      QuillEditor(
        theme="snow"
        v-model:content="editingNoteText"
        contentType="html"
        :toolbar="toolbarOptions"
      )
    template(#footer)
      BButton(variant="outline-secondary" @click="closeEditModal") Отмена
      BButton(variant="success" @click="saveEditedNote") 💾 Сохранить
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import {
  BAlert,
  BBadge,
  BButton,
  BCard,
  BCardBody,
  BCardTitle,
  BCardText,
  BCol,
  BContainer,
  BForm,
  BFormGroup,
  BFormTextarea,
  BModal,
  BRow,
  BSpinner,
  BFormInput
} from 'bootstrap-vue-next'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://54.84.204.161:8000'
const notes = ref([])
const newNoteText = ref('')
const editingNote = ref(null)
const editingNoteText = ref('')
const isEditModalOpen = ref(false)
const loading = ref(false)
const statusMessage = ref('')
const statusType = ref('success')
let refreshTimer = null
const searchQuery = ref('')


// Настраиваем только те кнопки, которые вам нужны (Bold + списки)
const toolbarOptions = [
  ['bold', 'italic', 'underline'], // Форматирование текста
  [{ 'list': 'ordered'}, { 'list': 'bullet' }], // Списки
  ['clean'] // Кнопка очистки форматирования
]

onMounted(() => {
  loadNotes()
  refreshTimer = setInterval(() => loadNotes(), 30000000) // 5 минут
})

onBeforeUnmount(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

async function loadNotes() {
  loading.value = true

  let url = `${API_BASE}/notes`

  if (searchQuery.value) {
    const params = new URLSearchParams({ search: searchQuery.value })
    url += `?${params.toString()}` // Получится /notes?search=ваштекст
  }

  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Failed to load notes')
    }

    const data = await response.json()
    notes.value = data.notes.map((note) => ({
      ...note,
      created_at: new Date(note.created_at),
      updated_at: new Date(note.updated_at)
    }))
  } catch (error) {
    console.error('Error loading notes:', error)
    showStatus('Ошибка при загрузке заметок', 'error')
  } finally {
    loading.value = false
  }
}

async function createNote() {
  if (!newNoteText.value.trim()) {
    showStatus('Заметка не может быть пустой', 'error')
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: newNoteText.value })
    })

    if (!response.ok) {
      throw new Error('Failed to create note')
    }

    newNoteText.value = ''
    showStatus('✅ Заметка успешно создана!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error creating note:', error)
    showStatus('Ошибка при создании заметки', 'error')
  }
}

function editNote(note) {
  editingNote.value = { ...note }
  editingNoteText.value = note.text
  isEditModalOpen.value = true
}

function closeEditModal() {
  isEditModalOpen.value = false
  editingNote.value = null
  editingNoteText.value = ''
}

async function saveEditedNote() {
  if (!editingNote.value || !editingNoteText.value.trim()) {
    showStatus('Заметка не может быть пустой', 'error')
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes/${editingNote.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: editingNoteText.value })
    })

    if (!response.ok) {
      throw new Error('Failed to update note')
    }

    closeEditModal()
    showStatus('✅ Заметка успешно обновлена!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error updating note:', error)
    showStatus('Ошибка при обновлении заметки', 'error')
  }
}

async function deleteNote(noteId) {
  if (!confirm('Вы уверены? Эту заметку нельзя будет восстановить.')) {
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes/${noteId}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Failed to delete note')
    }

    showStatus('✅ Заметка успешно удалена!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error deleting note:', error)
    showStatus('Ошибка при удалении заметки', 'error')
  }
}

function showStatus(message, type) {
  statusMessage.value = message
  statusType.value = type

  setTimeout(() => {
    statusMessage.value = ''
  }, 4000)
}

function formatDate(date) {
  if (!date) {
    return ''
  }

  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

let searchTimeout = null
const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  searchTimeout = setTimeout(() => {
    loadNotes()
  }, 500) // Задержка в 500 мс после последнего ввода
}

</script>
