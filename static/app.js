const LLM_SERVICE_ENDPOINT = "./generate"
let submitButton = document.querySelector("#submit")
let promptTextInput = document.querySelector("#prompt")
let statusText = document.querySelector("#status")
let outputTextArea = document.querySelector("#output")

let clearStatus = () => (statusText.textContent = "")
let setStatus = (content) => (statusText.textContent = content)
let clearOutput = () => (outputTextArea.textContent = "")
let setOutput = (content) => (outputTextArea.textContent = content)

submitButton.addEventListener("click", async () => {
	let startTime = new Date().getTime()

	let interval = setInterval(() => {
		let timeLapsed = ((new Date().getTime() - startTime) / 1000).toFixed(2)
		setStatus(`Running LiteLLM... (${timeLapsed}s)`)
	})

	let inputText = promptTextInput.value
	if (inputText.trim() == "") return

	let [response, error] = await getResponse(inputText)

	if (error) {
		setStatus("Error occured while generating text")
		return
	}

	let endTime = new Date().getTime()
	let timeTaken = (endTime - startTime) / 1000

	setOutput(response)

	setStatus(`Done in ${timeTaken} seconds`)
	clearInterval(interval)
})

promptTextInput.addEventListener("keyup", (event) => {
	clearStatus()
	clearOutput()
	if (event.keyCode == 13) {
		event.preventDefault()
		submitButton.click()
	}
})

async function getResponse(prompt) {
	try {
		let endpoint = `${LLM_SERVICE_ENDPOINT}?prompt=${prompt}`
		let response = await fetch(endpoint)
		let data = await response.text()
		data = JSON.parse(data)
		return [data.response, null]
	} catch (error) {
		return [null, error]
	}
}

const fetchData = () => {
	fetch("/stream?prompt=what is artificial intelligence") // Replace '/stream' with the appropriate URL endpoint
		.then((response) => {
			const reader = response.body.getReader()

			const processStream = ({ done, value }) => {
				if (done) {
					console.log("Streaming complete")
					return
				}

				// Process each chunk of data received from the server
				const data = new TextDecoder().decode(value)
				console.log("Received data:", data)

				// Continue reading the stream
				reader.read().then(processStream)
			}

			// Start reading the stream
			reader.read().then(processStream)
		})
		.catch((error) => {
			console.error("Error:", error)
		})
}

