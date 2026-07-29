window.onload = loadStudents();

document.getElementById("studentForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent page reload

    const name = document.getElementById("username").value;
    const age = document.getElementById("age").value;
    const email = document.getElementById("email").value;
    const course = document.getElementById("course").value;
    const student_id = document.getElementById("student_id").value;

    const student = {
        id:parseInt(student_id),
        name:name,
        age: parseInt(age),
        email: email,
        course:course
    };
    if (student_id .trim() === "") {
    url = "http://127.0.0.1:8000/students";
    method = "POST";
} else {
    url = `http://127.0.0.1:8000/students/${student_id}`;
    method = "PUT";

}
        fetch(url,{
        method:method,
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(student)
        })
    .then(response=>response.json())
    .then(data => {
        // console.log("Created:", data);
        alert("Success...!");
        document.getElementById("studentForm").reset();
        loadStudents();
        })   
    .catch(error =>{
        alert ("Error occurs",error);
    })
});


function loadStudents() {
    fetch("http://127.0.0.1:8000/students/")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("studentTable");
            tableBody.innerHTML = "";

            data.forEach(student => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.age}</td>
                        <td>${student.email}</td>
                        <td>${student.course}</td>
                        <td><button id="edit_${student.id}" class="edit">Edit</button>
                        <button id="delete_${student.id}"class ="delete">Delete</button></td>
                    </tr>`;
            });
        });
}


document.addEventListener("click", function (event) {

    if (event.target.classList.contains("edit")) {

        const studentId = event.target.id.split("_")[1];
        const row = event.target.closest("tr");

        const cells = row.getElementsByTagName("td");

        document.getElementById("student_id").value = cells[0].textContent;
        document.getElementById("username").value = cells[1].textContent;
        document.getElementById("age").value = cells[2].textContent;
        document.getElementById("email").value = cells[3].textContent;
        document.getElementById("course").value = cells[4].textContent;

    } else if (event.target.classList.contains("delete")) {

        const student_id = event.target.id.split("_")[1];

        if (!confirm("Are you sure you want to delete this student?")) {
            return;
        }

        fetch(`http://127.0.0.1:8000/students/${student_id}`, {
            method: "DELETE"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Delete failed");
            }

            alert("Student deleted successfully");

            // Remove the deleted row from the table
            event.target.closest("tr").remove();
        })
        .catch(error => {
            console.error(error);
            alert("Error deleting student");
        });
    }

});