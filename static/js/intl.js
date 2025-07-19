document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector("#telefone");
    if(input) {
        window.intlTelInput(input, {
            onlyCountries: ["br"],
            allowDropdown: false,
            showFlags: false,
            strictMode: true,
            autoPlaceholder: "aggressive",
            formatAsYouType: true,
            formatOnDisplay: true,
            countrySearch: false,
        });
    }
});