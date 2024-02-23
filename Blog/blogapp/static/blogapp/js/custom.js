
setTimeout(function(){
    $('#message').fadeOut('slow')
},4000)


// Function to display alert box only on the first visit
function displayFirstTimeAlert() {
var visited = localStorage.getItem('visited'); // Check if the user has visited the site before
if (!visited) {
    alert("जय श्री राम"); // Display the alert
    localStorage.setItem('visited', true); // Set flag in local storage to indicate the visit
}
}

// Call the function when the page loads
window.onload = function() {
displayFirstTimeAlert();
};


// JavaScript to handle form submission
document.getElementById('contact-form').addEventListener('submit', function(event) {
event.preventDefault(); // Prevent the default form submission

// Submit the form using AJAX
var formData = new FormData(this);
var xhr = new XMLHttpRequest();
xhr.open('POST', '{% url "Contact" %}', true);
xhr.onload = function() {
    if (xhr.status == 200) {
        // Show the thank you message box
        document.getElementById('thank-you-box').style.display = 'block';

        // Hide the thank you message box after 5 seconds
        setTimeout(function() {
            document.getElementById('thank-you-box').style.display = 'none';
            // Redirect to another page
            window.location.href = '{% url 'Contact' %}';  // Replace '/another-page' with the URL of the page you want to redirect to
        }, 4000);
    }
};
xhr.send(formData);
});