document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector("#phone");
    if(input) {
        window.intlTelInput(input, {
            utilsScript: "/static/intl-tel-input/build/js/utils.js",
            preferredCountries: ['br'],
            initialCountry: "br",
            separateDialCode: true,
            showFlags: true,
            allowDropdown: true,
            autoPlaceholder: "aggressive",
            customPlaceholder: function(selectedCountryPlaceholder, selectedCountryData) {
                return "Ex: " + selectedCountryPlaceholder;
            },
        });
    }
});