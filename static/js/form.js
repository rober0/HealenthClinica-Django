document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector("#phone");
    if(input) {
        window.intlTelInput(input, {
            initialCountry: "br",
            separateDialCode: true,
            autoPlaceholder: "aggressive",
            strictMode: true,
        });
    }
});