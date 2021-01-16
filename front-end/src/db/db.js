import * as env from "../../env.js"
const url = `http://localhost:${env.SERVER_PORT}`
export const insertMessage = async (messageText) => {
  console.log(messageText)
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
