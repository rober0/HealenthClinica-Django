import imask from 'imask';

document.addEventListener('DOMContentLoaded', function() {
    const telefoneInput = document.querySelector("#telefone");
    const cpfInput = document.querySelector("#cpf"); 
    const cepInput = document.querySelector("#cep");
    const crmInput = document.querySelector("#crm_numero");

    if (telefoneInput) {
        const telefoneMask = imask(telefoneInput, {
            mask: '(00) 00000-0000'
        });
    }
    if (cpfInput) {
        const cpfMask = imask(cpfInput, {
            mask: '000.000.000-00'
        });
    }
    if (cepInput) {
        const cepMask = imask(cepInput, {
            mask: '00000-000'
        });
    }
    if (crmInput) {
        const crmMask = imask(crmInput, {
            mask: '000000'
        });
    }
});