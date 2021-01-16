import * as env from "../../env.js"
const url = `http://localhost:${env.SERVER_PORT}`
export const insertMessage = async (messageText) => {
  const body = {
    text: messageText,
  }

  const options = {
    method: "POST",
    body: JSON.stringify(body),
  }
  const response = await fetch(url + "/insertMessage", options)
  const json = await response.json()
  return json
}

export const getMessages = async () => {
  const options = {
    method: "GET",
  }
  const response = await fetch(url + "/getMessages", options)
  const json = await response.json()
  return json
}

getMessages()
