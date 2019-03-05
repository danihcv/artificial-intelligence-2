let brain;

let training_data_xor = [
    {
        inputs: [0, 0],
        targets: [0]
    },
    {
        inputs: [0, 1],
        targets: [1]
    },
    {
        inputs: [1, 0],
        targets: [1]
    },
    {
        inputs: [1, 1],
        targets: [0]
    }
];

function getAnwser(outputs) {
    return Math.round(outputs[0], 0);
}

function setup() {
    brain = new NeuralNetwork(2, 1);
    brain.addHiddenLayer(3);
    brain.addHiddenLayer(10);

    for (let i = 0; i < 50000; i++) {
        const data = random(training_data_xor);
        brain.train(data.inputs, data.targets);
    }

    console.log('[0,0]', getAnwser(brain.predict([0, 0])));
    console.log('[0,1]', getAnwser(brain.predict([0, 1])));
    console.log('[1,0]', getAnwser(brain.predict([1, 0])));
    console.log('[1,1]', getAnwser(brain.predict([1, 1])));
}

function draw() {
    // put drawing code here
}