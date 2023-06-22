const LLM_SERVICE_ENDPOINT = "http://localhost:8000/generate"
let statusText = document.querySelector("#status")
let outputTextArea = document.querySelector("#output")

let clearStatus = () => statusText.textContent = ""
let setStatus = (content) => statusText.textContent = content
let clearOutput = () =>	outputTextArea.textContent = ""

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

prompt.addEventListener("keyup", (event) => {
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
