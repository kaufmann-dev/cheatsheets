function randomIntFromInterval(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function hasScrollbar(element) {
    return element.scrollHeight > element.clientHeight;
}

function clickToggle(element, firstHandler, secondHandler) {
    let useSecondHandler = false;

    element.addEventListener("click", (event) => {
        const handler = useSecondHandler ? secondHandler : firstHandler;
        useSecondHandler = !useSecondHandler;
        handler.call(element, event);
    });
}

function filterByText(input, elements) {
    const query = input.value.toLowerCase();

    elements.forEach((element) => {
        const matches = element.textContent.toLowerCase().includes(query);
        element.hidden = !matches;
    });
}
