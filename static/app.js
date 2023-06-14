let submit = document.querySelector("#submit")
let prompt = document.querySelector("#prompt")
let statusText = document.querySelector("#status")
let outputTextArea = document.querySelector("#output")

submit.addEventListener("click", async () => {
	let inputText = prompt.value
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
		let response = await fetch(`http://localhost:8000/generate?prompt=${prompt}`)
		let data = await response.json()
		return [data.response, null]
	} catch (error) {
		return [null, error]
	}
}
