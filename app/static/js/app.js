// static/js/app.js

document.addEventListener("DOMContentLoaded", function () {
    const viewForm = document.querySelector("form[action='/timetable/view']");  // Match form selector
  
    if (viewForm) {
      viewForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const classIdInput = this.querySelector("input[name='class_id']");
        const classId = classIdInput.value;
  
        if (!classId || isNaN(classId)) {
          alert("Please enter a valid Class ID.");
          return;
        }
  
        const url = `/timetable/${classId}`;
        window.location.href = url;
      });
    }
  });
