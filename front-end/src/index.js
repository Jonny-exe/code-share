import * as db from "./db/db.js"
import * as functions from "./functions.js"
const setButtonEventListeners = () => {
  document.querySelectorAll("button").forEach((item) => {
    item.addEventListener("click", (event) => {
      item.classList.add("animation")
      setTimeout(() => item.classList.remove("animation"), 500)
    })
  })

  document.querySelector("#sendMessageButton")
}

const init = async () => {
  functions.renderMessages()
  setButtonEventListeners()
  await db.insertMessage("LOLOL")
}

await init()
