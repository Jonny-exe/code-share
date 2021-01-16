import * as consts from "./consts/consts.js"
export const renderMessages = (items) => {
  items = [{ text: "Hi" }, { text: "añlskdjf" }]

  const createMessages = () => {
    let messages = ""
    items.forEach((item) => {
      console.log("Hi")
      let message = `<div class="message"><p>${item.text}</p> ${consts.messageButtons} </div><hr>`
      messages += message
    })
    return messages
  }

  const appendMessages = () => {
    document.getElementById("messagesWrapper").innerHTML = messages
  }

  const messages = createMessages()
  appendMessages(messages)
}
