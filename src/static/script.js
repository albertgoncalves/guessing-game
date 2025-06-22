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

function getElement(id) {
    const element = document.getElementById(id);
    if (element === null) {
        throw new Error();
    }
    return element;
}

function draw(canvas, context, consec, weights) {
    context.clearRect(0, 0, canvas.width, canvas.height);

    const width = canvas.width / (weights[0].consec + 1);

    context.beginPath();
    for (let weight of weights) {
        context.rect(weight.consec * width, canvas.height, width, (-weight.weight) * canvas.height);
    }
    context.fill();

    const x = (consec * width) + (width / 2);

    context.beginPath();
    context.moveTo(x, 0);
    context.lineTo(x, canvas.height);
    context.stroke();
}

window.onload = function() {
    post(function(next) {
        console.log(next);

        const canvas = getElement("canvas");
        const context = canvas.getContext("2d");
        context.imageSmoothingEnabled = false;

        context.fillStyle = "hsl(0, 0%, 90%)";
        context.strokeStyle = "hsl(5, 35%, 50%)";
        context.lineWidth = 5;

        const question = getElement("question");
        const answer = getElement("answer");
        const feedback = getElement("feedback");

        let selected = next;
        let response = null;

        question.textContent = selected.question;
        draw(canvas, context, selected.consec, selected.weights);

        answer.onkeyup = function(event) {
            if (event.keyCode !== 13) {
                return;
            }

            if (answer.value.trim() !== selected.answer) {
                feedback.textContent = selected.answer;
                if (response === null) {
                    response = answer.value.trim();
                }
                return;
            }

            post(function(next) {
                selected = next;
                response = null;

                question.textContent = selected.question;
                answer.value = "";
                feedback.textContent = "";
                draw(canvas, context, selected.consec, selected.weights);
            }, {previous: selected.question, response});
        };

        answer.focus();
    }, null);
};
