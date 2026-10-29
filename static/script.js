
const form = document.getElementById("studentForm");
const message = document.getElementById("message");
const studentList = document.getElementById("studentList");
const refreshButton = document.getElementById("refreshButton");

// Send student information to the backend
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    message.textContent = "Saving student...";

    try {
        const response = await fetch("/api/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Registration failed");
        }

        message.textContent = result.message;
        form.reset();

        await loadStudents();

    } catch (error) {
        message.textContent = error.message;
    }
});


// Retrieve saved students from the backend
async function loadStudents() {
    studentList.replaceChildren();

    try {
        const response = await fetch("/api/students");
        const students = await response.json();

        if (!response.ok) {
            throw new Error(students.error || "Could not load students");
        }

        if (students.length === 0) {
            const item = document.createElement("li");
            item.textContent = "No students registered yet.";
            studentList.appendChild(item);
            return;
        }

        students.forEach(function (student) {
            const item = document.createElement("li");
            item.textContent =
                `${student.name} — ${student.email}`;
            studentList.appendChild(item);
        });

    } catch (error) {
        message.textContent = error.message;
    }
}

refreshButton.addEventListener("click", loadStudents);

// Load existing records when the page opens
loadStudents();


fetch("/api/students", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, email })
});