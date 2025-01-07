const navMenuButton = document.querySelector(".nav-menu-button");
const navMenuButtonIcon = document.querySelector(".nav-menu-button > img");
const navList = document.querySelector(".nav-list");
const favoriteButton = document.querySelectorAll(".favorite-button");
const items = document.querySelectorAll("li a");

const toggleMenu = () => {
  navList.classList.toggle("open");
  if (navList.classList.contains("open")) {
    navMenuButton.classList.add("open");
    navMenuButtonIcon.src = "/week_1/assets/menu_close_icon.svg";
  } else {
    navMenuButton.classList.remove("open");
    navMenuButtonIcon.src = "/week_1/assets/menu_nav_icon.svg";
  }
};

const closeMenu = () => {
  if (navList.classList.contains("open")) {
    navList.classList.remove("open");
    navMenuButton.classList.remove("open");
    navMenuButtonIcon.src = "/week_1/assets/menu_nav_icon.svg";
  }
  return;
};

items.forEach((item) => {
  item.addEventListener("click", closeMenu);
});

favoriteButton.forEach((button) => {
  button.addEventListener("click", () => {
    button.classList.toggle("active");
  });
});

navMenuButton.addEventListener("click", toggleMenu);
