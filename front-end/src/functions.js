// import * as consts from "./consts/consts.js"
import * as db from "./db/db.js"

let currentMessages
let time = 0
setInterval(() => manageTime, 1000)
const manageTime = () => {
  time++
  if (time > 360) {
    db.didGiveLike(messages)
  }
}

export const renderMessages = (items) => {
  // I declare it so I dont have to make a request
  currentMessages = items
  const createMessages = () => {
    let messages = ""
    items.forEach((item) => {
      let messageItem = item.message
      const messageButtons = `<div class='messageButtonsWrapper'><button class='messageButtons' id="message${messageItem.id}"> ${messageItem.likes} </button></div>`
      let message = `<div class="message"><p>${messageItem.text}</p> ${messageButtons} </div>`
      messages += message
    })
    return messages
  }

  const restoreEventListners = () => {
    items.forEach((item) => {
      // Remove incase it already has one
      let messageItem = item.message
      let id = `#message${messageItem.id}`
      $(id).removeEventListener("click", () => like(messageItem, items))
      $(id).addEventListener("click", () => like(messageItem, items))
    })

    const like = async (item, items) => {
      let id = item.id
      item.timeToLike = time
      const newMessages = await db.addLike(id, items)
      renderMessages(newMessages)
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
