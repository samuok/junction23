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
        updateInfo('<h1>The idea</h1><p>Do you ever feel like time is slipping away? Have you pondered where the hours of your daily life vanish to? For all the curious minds out there, we\'ve got a solution just for you! All you need is a pair of Pixieray glasses and our Eyeviction toolkit.\n' +
            'Our toolkit analyzes data from the glasses and employs machine learning to identify the user\'s current activity. This opens up numerous possibilities for everyday use! For instance, imagine a user wanting to plan the upcoming week. With Eyeviction, they can visually assess how well they adhered to their weekly schedule.\n' +
            'In the scope of this project, we\'ve trained the application to recognize various activities, including driving, walking, reading, scrolling through social media, and chatting. The sky\'s the limit for further development!</p>');
    });

    button2.addEventListener('click', function() {
        updateInfo('<h1>Machine Learning</h1><p>Our model consist of RandomForest combined with our unique data structure. We start by grouping the input data into groups of 60 that we use to create our unique features. We train the model on this group features to identify different activities. Currently, our model boasts a 95% prediction accuracy based on the datasets that were provided. We split the dataset into a training, test and validation set consisting of 60% training, 20% testing and 20% validation. By doing this we ensure that the results are accurate.</p>');
    });

    button3.addEventListener('click', function() {
        updateInfo('<h1>Ideas for future</h1><p>As we have a fully working model and a way to use the datapoints, it would be possible to utilize day to day eye tracking data to summarize daily activities. That is only the first step. Upon further development the model could be trained a lot more to turn the data into real useful insights, such as:<br>- Improving concentration during studying<br>- Warning the user about driving, if too tired<br>- Highly modular program that can be easily further expanded to differentiate between new activities</p>');
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
        updateInfo('<h1>The team</h1><h3>Kerkko Kuokkanen, kerkko.kuokkanen@gmail.com<br><br>Jussi Ristolainen, jussimristolainen@gmail.com<br><br>Riku-Erik Mäki, rikuerik.maki@gmail.com<br><br>Samu Oksala, samu.oksala@hotmail.com</h3>');
    });

    // Function to update the info element content
    function updateInfo(data) {
        infoElement.innerHTML = data;
    }

    // Set the default content for the info element
    updateInfo('<h1>The idea</h1><p>Do you ever feel like time is slipping away? Have you pondered where the hours of your daily life vanish to? For all the curious minds out there, we\'ve got a solution just for you! All you need is a pair of Pixieray glasses and our Eyeviction toolkit.\n' +
        'Our toolkit analyzes data from the glasses and employs machine learning to identify the user\'s current activity. This opens up numerous possibilities for everyday use! For instance, imagine a user wanting to plan the upcoming week. With Eyeviction, they can visually assess how well they adhered to their weekly schedule.\n' +
        'In the scope of this project, we\'ve trained the application to recognize various activities, including driving, walking, reading, scrolling through social media, and chatting. The sky\'s the limit for further development!</p>');
});