"use strict";

function post(callback, body) {
    fetch(
        "/next",
        {method: "POST", body: JSON.stringify(body), headers: {"Content-Type": "application/json"}})
        .then(function(response) {
            return response.json();
        })
        .then(callback);
}

window.onload = function() {
    post(function(next) {
        let selected = next;
        let response = null;

        const question = document.getElementById("question");
        const answer = document.getElementById("answer");
        const feedback = document.getElementById("feedback");

        question.textContent = selected.question;

        answer.onkeyup = function(event) {
            if (answer.value !== selected.answer) {
                if (!selected.answer.startsWith(answer.value)) {
                    feedback.textContent = selected.answer;
                    if (response === null) {
                        response = answer.value;
                    }
                }
                return;
            }

            post(function(next) {
                selected = next;
                response = null;

                question.textContent = selected.question;
                answer.value = "";
                feedback.textContent = "";
            }, {previous: selected.question, response});
        };

        answer.focus();
    }, null);
};
