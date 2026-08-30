<template lang="pug">
BContainer.py-4.body
  BCard.shadow-sm.border-0
    BCardBody.p-4
      .d-flex.flex-column.flex-md-row.align-items-md-center.justify-content-between.gap-3.mb-4
        h1.h3.mb-0 📝 My notes
        BBadge.bg-primary.rounded-pill.fs-6(v-if="!loading") {{ notes.length }} notes

      BAlert(
        v-model="statusVisible"
        :variant="statusType === 'success' ? 'success' : 'danger'"
        dismissible
      ) {{ statusMessage }}

      //- Search field
      BFormGroup.mb-4(label="Search notes")
        BFormInput(
          v-model="searchQuery"
          @input="handleSearch"
          placeholder="Enter text to search..."
          type="search"
        )

      BForm(@submit.prevent="createNote")
        BFormGroup.mb-3(label="New note" label-for="new-note-text")
          BFormInput.mb-3(id="new-note-title" v-model="newNoteTitle" placeholder="Enter the note title..." required)
          QuillEditor(
            theme="snow"
            v-model:content="newNoteText"
            contentType="html"
            :toolbar="toolbarOptions"
            placeholder="Write a new note..."
          )

        .d-flex.justify-content-end
          BButton(variant="primary" type="submit" :disabled="loading") ➕ Add

      .text-center.py-5(v-if="loading")
        BSpinner(variant="primary" label="Loading notes")
        .mt-2 Loading notes...

      .text-center.py-5(v-else-if="notes.length === 0")
        .display-6 🎉
        p.mb-0 You don't have any notes yet

      BRow.g-3.mt-4.p-4(v-else)
        BCol(cols="12" md="6" lg="4" v-for="note in notes" :key="note.id")
          BCard(border-variant="primary" align="center" card-height="100%" class="h-100" :title="note.title")
            BCardSubtitle
              .small.text-muted.mb-2 📅 {{ formatDate(note.created_at) }}
              .small.text-muted(v-if="note.updated_at !== note.created_at") ✏️ {{ formatDate(note.updated_at) }}
            BCardText
              .ql-snow
                .ql-editor(v-html="note.text" contenteditable="true" style="padding: 0;")

            template(#footer)
              .d-flex.gap-2.justify-content-center
                BButton(variant="outline-primary" size="sm" @click="editNote(note)") ✏️ Edit
                BButton(variant="outline-danger" size="sm" @click="deleteNote(note.id)") 🗑️ Delete

  BModal(v-model="isEditModalOpen" title="Edit note" centered)
    BFormGroup(label="Note text")
      BFormInput.mb-3(id="new-note-title" v-model="editingNoteTitle" placeholder="Enter the note title..." required)
      QuillEditor(
        theme="snow"
        v-model:content="editingNoteText"
        contentType="html"
        :toolbar="toolbarOptions"
      )
    template(#footer)
      BButton(variant="outline-secondary" @click="closeEditModal") Cancel ❌
      BButton(variant="success" @click="saveEditedNote") 💾 Save
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, computed } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import {
  BAlert,
  BBadge,
  BButton,
  BCard,
  BCardBody,
  BCardTitle,
  BCardSubtitle,
  BCardText,
  BCol,
  BContainer,
  BForm,
  BFormGroup,
  BModal,
  BRow,
  BSpinner,
  BFormInput
} from 'bootstrap-vue-next'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://54.84.204.161:8000'
const notes = ref([])
const newNoteText = ref('')
const newNoteTitle = ref('')
const editingNote = ref(null)
const editingNoteTitle = ref('')
const editingNoteText = ref('')
const isEditModalOpen = ref(false)
const loading = ref(false)
const statusMessage = ref('')
const statusType = ref('success')
let refreshTimer = null
const searchQuery = ref('')
let statusVisible = computed(() => statusMessage.value !== '')


// Configure only the buttons you need (Bold + lists)
const toolbarOptions = [
  ['bold', 'italic', 'underline'], // Text formatting
  [{ 'list': 'ordered'}, { 'list': 'bullet' }], // Lists
  ['clean'] // Clear formatting button
]

onMounted(() => {
  loadNotes()
  refreshTimer = setInterval(() => loadNotes(), 400000)
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
    url += `?${params.toString()}` // Results in /notes?search=yourtext
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
    showStatus('Failed to load notes', 'error')
  } finally {
    loading.value = false
  }
}

async function createNote() {
  if (!newNoteTitle.value.trim()) {
    showStatus('The note title cannot be empty', 'error')
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: newNoteText.value, title: newNoteTitle.value })
    })

    if (!response.ok) {
      throw new Error('Failed to create note')
    }

    newNoteText.value = '<p><br></p>'
    newNoteTitle.value = ''
    showStatus('✅ Note created successfully!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error creating note:', error)
    showStatus('Failed to create note', 'error')
  }
}

function editNote(note) {
  editingNote.value = { ...note }
  editingNoteText.value = note.text
  editingNoteTitle.value = note.title
  isEditModalOpen.value = true
}

function closeEditModal() {
  isEditModalOpen.value = false
  editingNote.value = null
  editingNoteText.value = ''
  editingNoteTitle.value = ''
}

async function saveEditedNote() {
  if (!editingNote.value || !editingNoteText.value.trim() || !editingNoteTitle.value.trim()) {
    showStatus('The note title and text cannot be empty', 'error')
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes/${editingNote.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: editingNoteText.value, title: editingNoteTitle.value })
    })

    if (!response.ok) {
      throw new Error('Failed to update note')
    }

    closeEditModal()
    showStatus('✅ Note updated successfully!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error updating note:', error)
    showStatus('Failed to update note', 'error')
  }
}

async function deleteNote(noteId) {
  if (!confirm('Are you sure? This note cannot be restored.')) {
    return
  }

  try {
    const response = await fetch(`${API_BASE}/notes/${noteId}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Failed to delete note')
    }

    showStatus('✅ Note deleted successfully!', 'success')
    await loadNotes()
  } catch (error) {
    console.error('Error deleting note:', error)
    showStatus('Failed to delete note', 'error')
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

  return new Intl.DateTimeFormat('en-US', {
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
  }, 500) // 500 ms delay after the last input
}

</script>
