/* =========================
   AI GYM ASSISTANT
   FRONTEND CONTROLLER
========================= */

document.addEventListener(
"DOMContentLoaded",
()=>{

initializeTabs();
initializeDashboard();
initializeNavigation();

});

/* =========================
   LOGIN / REGISTER TABS
========================= */

function initializeTabs(){

const loginTab =
document.getElementById("loginTab");

const registerTab =
document.getElementById("registerTab");

const loginForm =
document.getElementById("loginForm");

const registerForm =
document.getElementById("registerForm");

loginTab.addEventListener(
"click",
()=>{

loginForm.style.display =
"block";

registerForm.style.display =
"none";

loginTab.classList.add(
"active"
);

registerTab.classList.remove(
"active"
);

});

registerTab.addEventListener(
"click",
()=>{

loginForm.style.display =
"none";

registerForm.style.display =
"block";

registerTab.classList.add(
"active"
);

loginTab.classList.remove(
"active"
);

});

}

/* =========================
   DEMO LOGIN
========================= */

function initializeDashboard(){

const loginBtn =
document.getElementById(
"demoLoginBtn"
);

const registerBtn =
document.getElementById(
"registerBtn"
);

if(loginBtn){

loginBtn.addEventListener(
"click",
loginUser
);

}

if(registerBtn){

registerBtn.addEventListener(
"click",
registerUser
);

}

}

/* =========================
   SIDEBAR NAVIGATION
========================= */

function initializeNavigation(){

const buttons =
document.querySelectorAll(
".nav-menu button"
);

buttons.forEach(btn=>{

btn.addEventListener(
"click",
()=>{

const page =
btn.dataset.page;

showPage(page);

});

});

}

/* =========================
   PAGE SWITCH
========================= */

function showPage(pageId){

document
.querySelectorAll(".page")
.forEach(page=>{

page.style.display="none";

});

const page =
document.getElementById(
pageId
);

if(page){

page.style.display="block";

}

}

/* =========================
   CARD ANIMATION
========================= */

function animateCards(){

const cards =
document.querySelectorAll(
".metric-card"
);

cards.forEach(
(card,index)=>{

card.style.opacity="0";

card.style.transform=
"translateY(40px)";

setTimeout(()=>{

card.style.transition=
".6s";

card.style.opacity="1";

card.style.transform=
"translateY(0px)";

},index*150);

});

}

/* =========================
   LOGOUT
========================= */

const logoutBtn =
document.getElementById(
"logoutBtn"
);

if(logoutBtn){

logoutBtn.addEventListener(
"click",
()=>{

document.getElementById(
"dashboard"
).style.display="none";

document.getElementById(
"loginScreen"
).style.display="flex";

});

}

const API =
"http://127.0.0.1:8000";

async function registerUser(){

const payload={

username:
document.getElementById(
"regUsername"
).value,

password:
document.getElementById(
"regPassword"
).value,

name:
document.getElementById(
"regName"
).value,

weight:
parseFloat(
document.getElementById(
"regWeight"
).value
),

height:
parseFloat(
document.getElementById(
"regHeight"
).value
),

goal:
document.getElementById(
"regGoal"
).value,

diet_preference:
document.getElementById(
"regDiet"
).value

};

try{

const response=
await fetch(
`${API}/auth/register`,
{
method:"POST",
headers:{
"Content-Type":
"application/json"
},
body:JSON.stringify(payload)
}
);

const data=
await response.json();

if(!response.ok){

throw new Error(
JSON.stringify(data)
);

}

alert(
"Registration Successful"
);

document
.getElementById(
"loginTab"
)
.click();

}
catch(error){

alert(
"Registration Failed"
);

console.error(error);

}

}

async function loginUser(){

const form=
new URLSearchParams();

form.append(
"username",
document.getElementById(
"loginUsername"
).value
);

form.append(
"password",
document.getElementById(
"loginPassword"
).value
);

try{

const response=
await fetch(
`${API}/auth/login`,
{
method:"POST",
headers:{
"Content-Type":
"application/x-www-form-urlencoded"
},
body:form
}
);

const data=
await response.json();

if(!response.ok){

throw new Error();

}

localStorage.setItem(
"token",
data.access_token
);

document.getElementById(
"loginScreen"
).style.display="none";

document.getElementById(
"dashboard"
).style.display="flex";

animateCards();

}
catch(error){

alert(
"Invalid Username or Password"
);

}

}