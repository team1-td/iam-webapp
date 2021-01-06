const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function(e){
    //toggle the type attribute
    const type = password.getAttribute('type') == 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    //toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});


//Credits

const creditsButton = document.querySelector(".credits");
const credits = document.querySelector(".credits__background");
const closeCredits = document.querySelector("#close__credits")
console.log(creditsButton)

function openCredits (){
    if (credits.style.display === "block") {
        credits.style.display = "none"
    } else {
        credits.style.display = "block"
    }
}

creditsButton.addEventListener("click", openCredits);
closeCredits.addEventListener("click", openCredits)