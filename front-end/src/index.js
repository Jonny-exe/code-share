import * as functions from "./functions.js"
document.querySelectorAll("button").forEach((item) => {
  item.addEventListener("click", (event) => {
    item.classList.add("animation")
    setTimeout(() => item.classList.remove("animation"), 500)
  })
})

functions.renderMessages()
