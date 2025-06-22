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

    const width = canvas.width / weights.length;

    context.beginPath();
    for (let i = 0; i < weights.length; ++i) {
        context.rect(i * width,
                     canvas.height,
                     width,
                     (-weights[(weights.length - 1) - i].weight) * canvas.height);
    }
    context.fill();

    for (let i = 0; i < weights.length; ++i) {
        if (consec === weights[(weights.length - 1) - i].consec) {
            const x = (i * width) + (width / 2);
            context.beginPath();
            context.moveTo(x, 0);
            context.lineTo(x, canvas.height);
            context.stroke();
            break;
        }
    }
}

window.onload = function() {
    post(function(next) {
        const question = getElement("question");
        const answer = getElement("answer");
        const feedback = getElement("feedback");

        let selected = next;
        let response = null;

        question.textContent = selected.question;

        const canvas = getElement("canvas");
        const context = canvas.getContext("2d");
        context.imageSmoothingEnabled = false;

        context.fillStyle = "hsl(0, 0%, 90%)";
        context.strokeStyle = "hsl(5, 35%, 50%)";
        context.lineWidth = 5;

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
