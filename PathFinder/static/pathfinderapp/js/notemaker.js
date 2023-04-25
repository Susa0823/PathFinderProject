showNotes();

const addNoteBtn = document.getElementById("addNote");

addNoteBtn.addEventListener("click", () => {
    // Getting Title and Description
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    let notes = localStorage.getItem("notes");
    if (notes == null) {
        notesObj = [];
    } else {
        notesObj = JSON.parse(notes);
    }

    // Adding Note in notes 
    newNote = {
        "title": title,
        "description": description
    }

    notesObj.push(newNote);

    // Setting notes object in localstorage
    localStorage.setItem("notes", JSON.stringify(notesObj));
    showNotes();
});

function showNotes() {
    let notes = localStorage.getItem("notes");

    if (notes == null) {
        notesObj = [];
    } else {
        notesObj = JSON.parse(notes);
    }

    let cardsGroup = "";

    // Getting Notes object and generating notes cards group

    notesObj.forEach(function (element, index) {
        cardsGroup += `<div class="card border-primary m-3" style="max-width: 18rem;">
                <div class="card-header fw-bold" id="cardTitle">${element.title}</div>
                <div class="card-body text-primary"><p class="card-text">${element.description}</p></div>
                <div class="container-fluid p-0 pb-2"><button class="btn btn-danger" id="${index}" onclick="deleteNote(${this.id})">Delete</button></div></div>`;
    });
    let notesContainer = document.getElementById("notesContainer");

    if (notesObj.length != 0) {
        notesContainer.innerHTML = cardsGroup;
    } else {
        notesContainer.innerHTML = ``;
        // notesContainer.innerHTML = `<b class="text-danger">No notes added yet<br>Please Add Some Notes!</b>`;
    }
    
}

function deleteNote(index) {
    let notes = localStorage.getItem("notes");

    if (notes == null) {
        notesObj = [];
    } else {
        notesObj = JSON.parse(notes);
    }

    // Find the index of the note based on its content
    let noteIndex = -1;
    for (let i = 0; i < notesObj.length; i++) {
        if (notesObj[i].content === notesObj[index].content) {
            noteIndex = i;
            break;
        }
    }

    if (noteIndex === -1) {
        console.error("Note not found.");
        return;
    }

    // Deleting Note
    notesObj.splice(noteIndex, 1);
    localStorage.setItem("notes", JSON.stringify(notesObj));
    showNotes();
}




// function deleteNote(index) {
//     let notes = localStorage.getItem("notes");

//     if (notes == null) {
//         notesObj = [];
//     } else {
//         notesObj = JSON.parse(notes);
//     }// Deleting Note
//     notesObj.splice(index, 1);
//     localStorage.setItem("notes", JSON.stringify(notesObj));
//     showNotes();
// }