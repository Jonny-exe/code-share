import * as consts from "./consts/consts.js"
import * as db from "./db/db.js"
export const renderMessages = (items) => {
  const createMessages = () => {
    let messages = ""
    items.forEach((item) => {
      const messageButtons = `<div class='messageButtonsWrapper'><button class='messageButtons' id="message${item.id}"> ${item.likes} </button></div>`
      let message = `<div class="message"><p>${item.text}</p> ${messageButtons} </div>`
      messages += message
    })
    return messages
  }

  const restoreEventListners = (target) => {
    items.forEach((item) => {
      // Remove incase it already has one
      let id = `#message${item.id}`
      $(id).removeEventListener("click", () => db.addLike(item.id))
      $(id).addEventListener("click", () => db.addLike(item.id))
    })

    const like = async (id) => {
      await db.addLike(id)
      // await db.
    }
  }

  const appendMessages = () => {
    $("#messagesWrapper").innerHTML = messages
  }

  const messages = createMessages()
  appendMessages(messages)
  restoreEventListners()
}

export const $ = (item) => {
  return document.querySelector(item)
}
