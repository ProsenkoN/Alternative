function addTask() {

    var input = document.getElementById("taskInput");
    var value = input.value;

    fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            task: value
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        location.reload();
    });

}