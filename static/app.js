const LLM_SERVICE_ENDPOINT = "http://localhost:8000/generate"
let submitButton = document.querySelector("#submit")
let promptTextInput = document.querySelector("#prompt")
let statusText = document.querySelector("#status")
let outputTextArea = document.querySelector("#output")

let clearStatus = () => statusText.textContent = ""
let setStatus = (content) => statusText.textContent = content
let clearOutput = () =>	outputTextArea.textContent = ""

submitButton.addEventListener("click", async () => {
	
	let inputText = promptTextInput.value
	if(inputText.trim() == "") return
	statusText.innerHTML = "Tokenizing your input..."

	let [response, error] = await getResponse(inputText)

	if(error) {
		statusText.innerHTML = "Error occured while generating text"
		return
	}

	outputTextArea.innerHTML = response

	statusText.innerHTML = "Done!"
})

promptTextInput.addEventListener("keyup", (event) => {
	if(event.keyCode == 13) {
		event.preventDefault()
		submit.click()
	}
})


async function getResponse(prompt) {
	try {
		let endpoint = `${LLM_SERVICE_ENDPOINT}?prompt=${prompt}`
		let response = await fetch(endpoint)
		let data = await response.json()
		return [data.response, null]
	} catch (error) {
		return [null, error]
	}
}
