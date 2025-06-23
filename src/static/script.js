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

function draw(canvasWeights, contextWeights, canvasSizes, contextSizes, consec, weights) {
    contextWeights.clearRect(0, 0, canvasWeights.width, canvasWeights.height);
    contextSizes.clearRect(0, 0, canvasSizes.width, canvasSizes.height);

    const width = canvasWeights.width / weights.length;

    contextWeights.beginPath();
    contextSizes.beginPath();
    for (let i = 0; i < weights.length; ++i) {
        contextWeights.rect(i * width,
                            canvasWeights.height,
                            width,
                            (-weights[(weights.length - 1) - i].weight) * canvasWeights.height);

        contextSizes.rect(i * width,
                          canvasSizes.height,
                          width,
                          (-weights[(weights.length - 1) - i].size) * canvasSizes.height);
    }
    contextWeights.fill();
    contextSizes.fill();

    for (let i = 0; i < weights.length; ++i) {
        if (consec === weights[(weights.length - 1) - i].consec) {
            const x = (i * width) + (width / 2);

            contextWeights.beginPath();
            contextWeights.moveTo(x, 0);
            contextWeights.lineTo(x, canvasWeights.height);
            contextWeights.stroke();

            contextSizes.beginPath();
            contextSizes.moveTo(x, 0);
            contextSizes.lineTo(x, canvasSizes.height);
            contextSizes.stroke();
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

        const canvasWeights = getElement("canvas-weights");
        const contextWeights = canvasWeights.getContext("2d");
        contextWeights.imageSmoothingEnabled = false;

        contextWeights.fillStyle = "hsl(0, 0%, 90%)";
        contextWeights.strokeStyle = "hsl(5, 35%, 50%)";
        contextWeights.lineWidth = 5;

        const canvasSizes = getElement("canvas-sizes");
        const contextSizes = canvasSizes.getContext("2d");
        contextSizes.imageSmoothingEnabled = false;

        contextSizes.fillStyle = "hsl(0, 0%, 90%)";
        contextSizes.strokeStyle = "hsl(5, 35%, 50%)";
        contextSizes.lineWidth = 5;

        draw(canvasWeights,
             contextWeights,
             canvasSizes,
             contextSizes,
             selected.consec,
             selected.weights);

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
                draw(canvasWeights,
                     contextWeights,
                     canvasSizes,
                     contextSizes,
                     selected.consec,
                     selected.weights);
            }, {previous: selected.question, response});
        };

        answer.focus();
    }, null);
};
