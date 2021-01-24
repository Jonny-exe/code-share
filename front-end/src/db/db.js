import * as env from "../../env.js"
const url = `http://localhost:${env.SERVER_PORT}/`
export const insertMessage = async (messageText) => {
  const body = {
    message: {
      text: messageText,
      likes: 0,
      did_give_like: false,
    },
  }

  const options = {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  }
  const response = await fetch(url + "insert_message", options)
  const json = await response.json()
  return json
}

export const getMessages = async () => {
  const options = {
    method: "GET",
  }
  const response = await fetch(url + "get_messages", options)
  const json = await response.json()
  return json.messages
}

export const addLike = async (messageId, messages) => {
  const body = {
    id: messageId,
  }
  const options = {
    method: "POST",
    body: JSON.stringify(body),
  }
  const response = await fetch(url + "add_like", options)
  const json = await response.json()
  didGiveLike(messages, true)
  return json.messages
}

export const didGiveLike = async (messages) => {
  const body = {
    messages: messages,
  }
  const options = {
    method: "POST",
    body: JSON.stringify(body),
  }
  const response = await fetch(url + "did_give_like", options)
  const json = await response.json()
  return json
}
