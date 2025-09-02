import intlTelInput from "intl-tel-input/intlTelInputWithUtils";
import "intl-tel-input/build/css/intlTelInput.css";

document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector("#telefone");
    if(input) {
        intlTelInput(input, {
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