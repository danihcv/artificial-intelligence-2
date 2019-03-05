const desiredDigits = [2, 5, 8], trainsPerFrame = 10;

let mnist, brain, trainIndex = 0, isLooping = true, userDigit, times = 0, trainImage;
let trainImages = [], trainLabels = [], canTrain = false, hasUserData = false;

function setup() {
    createCanvas(400, 200).parent('container');
    userDigit = createGraphics(200, 200);
    trainImage = createImage(28, 28);

    brain = new NeuralNetwork(784, desiredDigits.length);
    brain.addHiddenLayer(16);
    brain.addHiddenLayer(16);

    loadMNIST((data) => {
        mnist = data;
        console.log(mnist);

        for (let i = 0; i < mnist.train_images.length; i++) {
            if (desiredDigits.includes(mnist.train_labels[i])) {
                trainImages.push(mnist.train_images[i]);
                trainLabels.push(mnist.train_labels[i]);
            }
        }
        console.log(trainImages);
        console.log(trainLabels);
        canTrain = true;
    });
}

function draw() {
    background(0);

    if (canTrain && mnist) {
        for (let i = 0; i < trainsPerFrame; i++) {
            trainIndex = Math.ceil(random(trainImages.length - 1));
            train(i === 0);
        }
    }

    guessUserDigit();

    image(userDigit, 0, 0);
    if (mouseIsPressed) {
        hasUserData = true;
        userDigit.stroke(255);
        userDigit.strokeWeight(select('#brushSize').value());
        userDigit.line(mouseX, mouseY, pmouseX, pmouseY);
    }

    stroke(255);
    line(200, 0, 200, 200);
}

function getAnswer(outputs) {
    let index = 0, max = outputs[0];
    for (let i = 1; i < outputs.length; i++) {
        if (outputs[i] > max) {
            max = outputs[i];
            index = i;
        }
    }
    return desiredDigits[index];
}

function train(drawTrainImage = false) {
    try {
        let inputs = [];

        if (drawTrainImage)
            trainImage.loadPixels();

        for (let i = 0; i < 784; i++) {
            let bright = trainImages[trainIndex][i];
            inputs[i] = bright / 255;

            if (drawTrainImage) {
                let index = i * 4;
                trainImage.pixels[index] = bright;
                trainImage.pixels[index + 1] = bright;
                trainImage.pixels[index + 2] = bright;
                trainImage.pixels[index + 3] = 255;
            }
        }

        if (drawTrainImage) {
            trainImage.updatePixels();
            image(trainImage, 200, 0, 200, height);
        }

        let label = trainLabels[trainIndex];
        let guess = getAnswer(brain.predict(inputs));

        select('#label').html(label);
        select('#guess').html(guess);

        if (label === guess) {
            select('#guess').class('correct');
        } else {
            select('#guess').class('wrong');
        }

        let targets = Array(desiredDigits.length).fill(0);
        targets[desiredDigits.findIndex((el) => el === label)] = 1;

        brain.train(inputs, targets);
        console.log('trained', ++times + '/' + trainImages.length, 'times. trandIndex:', trainIndex);
    } catch (e) {
        console.error('trainIndex:', trainIndex, 'trainImages.length', trainImages.length);
        console.error(e);
    }
}

function keyPressed() {
    if (key === 'r') {
        hasUserData = false;
        userDigit.background(0);
    } else if (key === 'p') {
        canTrain = !canTrain;
    } else if (key === ' ') {
        guessUserDigit(true);
    }
}

function guessUserDigit(popupGuess = false) {
    if (hasUserData) {
        let inputs = [];
        let img = userDigit.get();
        img.resize(28, 28);
        img.loadPixels();
        for (let i = 0; i < 784; i++) {
            inputs[i] = img.pixels[i * 4];
        }

        let guess = getAnswer(brain.predict(inputs));

        if (popupGuess) {
            alert('Eu acho que é um... ' + guess + '!');
        } else {
            select('#userGuess').html(guess);
        }
    } else {
        select('#userGuess').html('_')
    }
}
