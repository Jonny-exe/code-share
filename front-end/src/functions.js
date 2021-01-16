import * as consts from "./consts/consts.js"
export const renderMessages = (items) => {
  const createMessages = () => {
    let messages = ""
    items.forEach((item) => {
      console.log("Hi")
      if (item != "") {
        let message = `<div class="message"><p>${item}</p> ${consts.messageButtons} </div><hr>`
        messages += message
      }
    })
    return messages
  }

  const appendMessages = () => {
    document.getElementById("messagesWrapper").innerHTML = messages
  }

  const messages = createMessages()
  appendMessages(messages)
}

export const $ = (item) => {
  return document.querySelector(item)
}
