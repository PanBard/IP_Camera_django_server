function myFunction() {
    alert("Hello from a static file!");
  }

  const csrfToken = '{{ csrf_token }}'; // Ensure this renders correctly

function elo() {
    document.addEventListener('click', function(event) {
        const x = event.clientX; // Get X coordinate
        const y = event.clientY; // Get Y coordinate
        console.log(x,y);
        // Send the coordinates to Django backend
        fetch(window.capture_mouse_position_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': window.csrfToken // Include CSRF token for security
            },
            body: `x=${x}&y=${y}`
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    });
  }

