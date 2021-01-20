import * as db from "./db/db.js"
import * as functions from "./functions.js"

const setButtonEventListeners = () => {
  const buttons = document.querySelectorAll("button")
  buttons.forEach((item) => {
    item.addEventListener("click", (event) => {
      item.classList.add("animation")
      setTimeout(() => item.classList.remove("animation"), 500)
    })
  })

  functions.$("button.sendMessageInputs").addEventListener("click", sendMessage)
}

const sendMessage = async () => {
  const text = functions.$("textarea.sendMessageInputs").value
  await db.insertMessage(text)
}

const init = async () => {
  setButtonEventListeners()
  const messages = await db.getMessages()
  functions.renderMessages(messages)
}
init()
