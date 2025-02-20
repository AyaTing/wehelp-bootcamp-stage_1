const deleteButtons = document.querySelectorAll(".delete-button");

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
