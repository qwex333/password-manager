function validateForm() {
    var x = document.forms["register"]["password"].value;
    if (x == "") {
      alert("Name must be filled out");
      return false;
    }
  }