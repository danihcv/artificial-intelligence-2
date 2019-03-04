let brain;

let training_data = [
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

function setup() {
    brain = new NeuralNetwork(2, 1);
    brain.addHiddenLayer(3);
    brain.addHiddenLayer(10);

    for (let i = 0; i < 50000; i++) {
        const data = random(training_data);
        brain.train(data.inputs, data.targets);
    }

    console.log(brain.predict([0, 0]));
}

function draw() {
    // put drawing code here
}