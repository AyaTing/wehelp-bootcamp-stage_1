const deleteButtons = document.querySelectorAll(".delete-button");
const queryButton = document.querySelector(".member-query-button");
const queryInput = document.querySelector("#member-query");
const queryDisplay = document.querySelector(".member-query-display");
const updateButton = document.querySelector(".name-update-button");
const updateInput = document.querySelector("#name-update");
const updateResult = document.querySelector(".name-update-result");
const welcome = document.querySelector(".welcome");

const memberQuery = (e) => {
  e.preventDefault();
  const username = queryInput.value.trim();
  if (!username) {
    queryDisplay.textContent = "輸入欄位不得為空白";
    queryInput.value = "";
    return;
  }
  fetch(`/api/member?username=${username}`)
    .then((response) => response.json())
    .then((result) => {
      if (result.error) {
        queryDisplay.textContent = "無查詢權限，請重新登入";
        queryInput.value = "";
      } else if (result.data && result.data.id) {
        const userName = result.data.name;
        const userUsername = result.data.username;
        queryDisplay.textContent = `${userName}（${userUsername}）`;
      } else {
        queryDisplay.textContent = "查無此用戶";
        queryInput.value = "";
      }
    })
    .catch((error) => {
      console.log(error);
      queryDisplay.textContent = "查詢失敗，請稍後再試";
      queryInput.value = "";
    });
};

const nameUpdate = (e) => {
  e.preventDefault();
  const newName = updateInput.value.trim();
  if (!newName) {
    updateResult.textContent = "輸入欄位不得為空白";
    updateInput.value = "";
    return;
  }
  fetch("/api/member", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: newName,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result && result.ok) {
        updateResult.textContent = "更新成功";
        updateInput.value = "";
        welcome.textContent = `${newName}，歡迎登入系統`;
      } else {
        updateResult.textContent = "更新失敗";
        updateInput.value = "";
      }
    })
    .catch((error) => {
      console.log(error);
      updateResult.textContent = "更新程序錯誤，請稍後再試";
      updateInput.value = "";
    });
};

deleteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();
    if (confirm("確定刪除此留言？")) {
      const form = button.closest("form");
      form.submit();
    }
  });
});

window.onload = () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("success") === "true") {
    alert("註冊成功！");
    window.history.replaceState({}, "", "/");
  }
};

if (queryButton) {
  queryButton.addEventListener("click", memberQuery);
}
if (updateButton) {
  updateButton.addEventListener("click", nameUpdate);
}
