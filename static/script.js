document.addEventListener('DOMContentLoaded', function() {
    // Get references to buttons and info element
    var button1 = document.getElementById('button1');
    var button2 = document.getElementById('button2');
    var button3 = document.getElementById('button3');
    var button4 = document.getElementById('button4');
    var button5 = document.getElementById('button5');
    var infoElement = document.getElementById('info');

    // Add click event listeners to buttons
    button1.addEventListener('click', function() {
        updateInfo('<h1>The idea</h1><p>Our initial idea for the project was that we would create a machine learning model, that we could train with the given data and after that anyone could use their datasets from their glasses on our model. However, perhaps a bit late we came to the realization, that it would not be possible, because nearly noone has a proper dataset.' +
            ' Instead, what we came up with is: <br>- Eye tracking<br>- Machine Learning model to identify different activities<br>- A way to send requests to the server using single data points and use this to predict the activies using the trained model</p>');
    });

    button2.addEventListener('click', function() {
        updateInfo('<img src="">');
    });

    button3.addEventListener('click', function() {
        updateInfo('<h1>Ideas for future</h1><p>As we have a fully working model and a way to use the datapoints, it would be possible to utilize day to day eye tracking data to summarize daily activities. That is only the first step. Upon further development the model could be trained a lot more to turn the data into real useful insights, such as:<br>- Improving concentration during studying<br>- Warning the user about driving, if too tired<br>- Highly modular program that can be easily further expanded to differentiate between new activities</p>');
    });

    button4.addEventListener('click', function() {
        updateInfo('Data for Button 4');
    });

    button5.addEventListener('click', function() {
        updateInfo('Data for Button 5');
    });

    // Function to update the info element content
    function updateInfo(data) {
        infoElement.innerHTML = data;
    }

    // Set the default content for the info element
    updateInfo('Data for Button 1');
});