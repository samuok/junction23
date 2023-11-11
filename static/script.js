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
        updateInfo('Data for Button 1');
    });

    button2.addEventListener('click', function() {
        updateInfo('Data for Button 2');
    });

    button3.addEventListener('click', function() {
        updateInfo('Data for Button 3');
    });

    button4.addEventListener('click', function() {
        updateInfo('Data for Button 4');
    });

    button5.addEventListener('click', function() {
        updateInfo('Data for Button 5');
    });

    // Function to update the info element content
    function updateInfo(data) {
        infoElement.textContent = data;
    }
});
