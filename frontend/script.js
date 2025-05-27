const API_URL = "http://localhost:8000"

const form = document.getElementById("noteForm")
const notesDiv = document.getElementById("notes")

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const image = document.getElementById("image").files[0];

    const formData = new FormData();
    formData.append("title", title)
    formData.append("description", description);
    if (image) {
        formData.append("file", image)
    }

    await fetch(`${API_URL}/notes/`, {
        method: "POST",
        body: formData,
    });

    form.reset();
    loadNotes();
});

async function loadNotes() {
    const res = await fetch(`${API_URL}/notes/`);
    const notes = await res.json();

    notesDiv.innerHTML = "";
    notes.forEach((note) => {
        const div = document.createElement("div");
        div.className = "note";
        div.innerHTML = `
            <h3>${note.title}</h3>
            <p>${note.description}</p>
            ${note.image ? `<img src="${API_URL}/${note.image}" width="200">` : ""}
            <p>Concluído: ${note.completed}</p>
            <button onclick="deleteNote(${note.id})">Excluir</button>
        `;
        notesDiv.appendChild(div)
    })
}

async function deleteNote(id) {
    await fetch(`${API_URL}/notes/${id}`, { method: "DELETE" });
    loadNotes();
}

loadNotes();