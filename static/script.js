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
        updateInfo('<h3>Eye tracking algorithm</h3><p>The eye tracking algorithm follows the eyes movement \
                    and tracks the eyes convergence distance in cm. The algorithm treats each lense of the glasses as an unit circle \
                    with the sensors on the circumference. The data is translated to fit into the circle and then used to \
                    calculate the positions of the pupils. These positions can be then further used to check the direction of the eyes \
                    or to calculate a position in the surface of the unit sphere that represents the eyes view direction. \
                    These direction vectors from both eyes can be then used to calculate the view distance so that \
                    they can be used as data for our machine learning model.</p>');
    });

    button5.addEventListener('click', function() {
        updateInfo('Data for Button 5');
    });

    // Function to update the info element content
    function updateInfo(data) {
        infoElement.innerHTML = data;
    }
});
