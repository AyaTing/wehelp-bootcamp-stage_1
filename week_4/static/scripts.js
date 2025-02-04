const signInForm = document.querySelector(".sign-in-form");
const checkbox = document.querySelector("#terms");
const calculateForm = document.querySelector(".calculate-form");
const inputElement = document.querySelector("#positive-integer-input");

const checkPositiveInteger = (e) => {
  e.preventDefault();
  const inputValue = inputElement.value * 1;
  if (Number.isInteger(inputValue) && inputValue > 0) {
    displayResult(inputValue);
    return inputValue;
  } else {
    inputElement.value = "";
    alert("Please enter a positive number.");
  }
};

const displayResult = (number) => {
  window.location.href = `/square/${number}`;
};

calculateForm.addEventListener("submit", checkPositiveInteger);

signInForm.addEventListener("submit", (e) => {
  if (!checkbox.checked) {
    e.preventDefault();
    alert("Please check the checkbox first.");
  }
});
