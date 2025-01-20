const navMenuButton = document.querySelector(".nav-menu-button");
const navMenuButtonIcon = document.querySelector(".nav-menu-button > img");
const navList = document.querySelector(".nav-list");
const items = document.querySelectorAll("li a");
const url =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
const cardContainer = document.querySelector(".card-container");
const loadMoreButton = document.querySelector(".load-more-button");
let spots = [];

const toggleMenu = () => {
  navList.classList.toggle("open");
  if (navList.classList.contains("open")) {
    navMenuButton.classList.add("open");
    navMenuButtonIcon.src = "assets/menu_close_icon.svg";
  } else {
    navMenuButton.classList.remove("open");
    navMenuButtonIcon.src = "assets/menu_nav_icon.svg";
  }
};

const closeMenu = () => {
  if (navList.classList.contains("open")) {
    navList.classList.remove("open");
    navMenuButton.classList.remove("open");
    navMenuButtonIcon.src = "assets/menu_nav_icon.svg";
  }
  return;
};

fetch(url)
  .then((response) => response.json())
  .then((data) => {
    spots = data.data.results;
    renderPromotions(spots.splice(0, 3));
    renderCards(spots.splice(0, 10));
    return spots;
  })
  .catch((error) => {
    console.log(error);
  });

const renderPromotions = (spots) => {
  const promotionContainer = document.querySelector(".promotion-container");
  spots.forEach((spot) => {
    const promotion = document.createElement("article");
    promotion.className = "promotion";
    const promotionContent = document.createElement("h3");
    promotionContent.className = "promotion-content";
    promotionContent.textContent = spot.stitle;
    const promotionImage = document.createElement("img");
    promotionImage.className = "promotion-image";
    const photos = spot.filelist
      .toLowerCase()
      .split(".jpg")
      .map((photo) => {
        return (photo = photo + ".jpg");
      });
    promotionImage.src = photos[0];
    promotion.appendChild(promotionImage);
    promotion.appendChild(promotionContent);
    promotionContainer.appendChild(promotion);
  });
};

const renderCards = (spots) => {
  spots.forEach((spot) => {
    const card = document.createElement("figure");
    card.className = "card";
    const favoriteButton = document.createElement("button");
    favoriteButton.className = "favorite-button";
    const favoriteIcon = document.createElement("img");
    favoriteIcon.src = "assets/star_icon.svg";
    favoriteButton.appendChild(favoriteIcon);
    const cardImage = document.createElement("img");
    cardImage.className = "card-image";
    const photos = spot.filelist
      .toLowerCase()
      .split(".jpg")
      .map((photo) => {
        return (photo = photo + ".jpg");
      });
    cardImage.src = photos[0];
    const cardTitle = document.createElement("figcaption");
    cardTitle.className = "card-title";
    cardTitle.textContent = spot.stitle;
    card.appendChild(favoriteButton);
    card.appendChild(cardImage);
    card.appendChild(cardTitle);
    cardContainer.appendChild(card);
  });
};

const loadMoreCards = () => {
  renderCards(spots.splice(0, 10));
  if (spots.length === 0) {
    loadMoreButton.style.display = "none";
  }
};

navMenuButton.addEventListener("click", toggleMenu);
items.forEach((item) => {
  item.addEventListener("click", closeMenu);
});
loadMoreButton.addEventListener("click", loadMoreCards);
cardContainer.addEventListener("click", (e) => {
  if (e.target.classList.contains("favorite-button")) {
    e.target.classList.toggle("active");
  }
});
