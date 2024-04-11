const form = document.getElementById('form');
const fullName = document.getElementById('fullName');
const cardNumber = document.getElementById('cardNumber');
const expirationDate = document.getElementById('expirationDate');
const cardCCV = document.getElementById('cardCCV');

form.addEventListener('submit', e => {
    e.preventDefault();

    validateInputs();
    redirectFunction();
});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const isValidcardNumber = cardNumber => {
    const re = /^(?:\d[ -]*?){16}$/;
    return re.test(String(cardNumber).toLowerCase());
}

const isValidexpirationDate = expirationDate => {
    const re = /^(?:\d[ /]*?){4}$/;
    return re.test(String(expirationDate).toLowerCase());
}

const isValidcardCCV = cardCCV => {
    const re = /^(?:\d[ /]*?){3}$/;
    return re.test(String(cardCCV).toLowerCase());
}

const validateInputs = () => {
    const fullNameValue = fullName.value.trim();
    const cardNumberValue = cardNumber.value.trim();
    const expirationDateValue = expirationDate.value.trim();
    const cardCCVValue = cardCCV.value.trim();

    if(fullNameValue === '') {
        setError(fullName, 'Full Name is required');
    } else {
        setSuccess(fullName);
    }

    if(cardNumberValue === '') {
        setError(cardNumber, 'Credit Card Number is required');
    } else if (!isValidcardNumber(cardNumberValue)) {
        setError(cardNumber, 'Provide a valid Credit Card Number');
    } else {
        setSuccess(cardNumber);
    }

    if(expirationDateValue === '') {
        setError(expirationDate, 'Card Expiration Date is required');
    } else if (!isValidexpirationDate(expirationDateValue)) {
        setError(expirationDate, 'Provide a valid Expiration Date')
    } else {
        setSuccess(expirationDate);
    }

    if(cardCCVValue === '') {
        setError(cardCCV, 'Card CCV is required');
    } else if (!isValidcardCCV(cardCCVValue)) {
        setError(cardCCV, "Provide a valid card CCV");
    } else {
        setSuccess(cardCCV);
    }

};
function redirectFunction(){
    window.location.href = "{% url 'checkOutConfirm' %}"
}
