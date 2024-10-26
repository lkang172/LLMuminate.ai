const start = () => {
  let output = document.createElement("p");
  output.id = "#message";
  let title = document.querySelector("#title");

  chrome.tabs
    .query({ active: true, currentWindow: true })
    .then(function (tabs) {
      let activeTab = tabs[0];
      let activeTabId = activeTab.id;

      return chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: DOMtoString,
      });
    })
    .then(async function (results) {
      let html = results[0].result;
      let parser = new DOMParser();
      let doc = parser.parseFromString(html, "text/html");

      if (
        doc
          .querySelector("meta[property='og:title']")
          .getAttribute("content") == "ChatGPT"
      ) {
        let convo = [];
        let i = 2;
        while (
          doc.querySelector(
            'article[data-testid="conversation-turn-' + i + '"]'
          ) != undefined
        ) {
          convo.push(
            doc.querySelector(
              'article[data-testid="conversation-turn-' + i + '"]'
            )
          );
          ++i;
        }
        document.body = await factCheck(convo[convo.length - 1].textContent);
      } else if (
        doc.querySelector("title").textContent.search("Claude") != -1
      ) {
        document.body = await factCheck(
          doc
            .querySelector('div[data-test-render-count="1"]')
            .getElementsByClassName("font-claude-message")[0].textContent
        );
      } else if (
        doc
          .querySelector("meta[property='og:site_name']")
          .getAttribute("content") == "Gemini"
      ) {
        let responses = doc.querySelectorAll("message-content");
        document.body = await factCheck(
          responses[responses.length - 1].textContent
        );
      } else {
        throw new Error("");
      }
    })
    .catch(async function (error) {
      const textInput = document.createElement("textarea");
      textInput.id = "text-input";
      textInput.className = "scrollable-box";
      const button = document.createElement("button");
      button.textContent = "Submit";
      button.id = "submit";
      button.className = "center";
      button.addEventListener("click", async () => {
        document.body.removeChild(textInput);
        document.body.removeChild(button);
        document.body.removeChild(title);
        document.body = await factCheck(textInput.value);
      });
      document.body.appendChild(textInput);
      document.body.appendChild(button);
      title.innerText =
        "No prompt from Claude, Gemini, or ChatGPT detected. Please enter the information you want to fact check.";
    });
};
alreadyStarted = false;

if (!alreadyStarted) window.onload = start;

const DOMtoString = (selector) => {
  if (selector) {
    selector = document.querySelector(selector);
    if (!selector) return "ERROR: querySelector failed to find node";
  } else {
    selector = document.documentElement;
  }
  return selector.outerHTML;
};

const factCheck = async (input) => {
  const apiUrl = "http://127.0.0.1:5000/api/message";

  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input }),
  };

  return fetch(apiUrl, requestOptions)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      container = document.createElement("body");
      container.appendChild(formatSimilarityScore(data.similarity_assessment));
      container.appendChild(formatFactChecks(data.fact_checks));
      return container;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const formatSimilarityScore = (similarityScore) => {
  simcontainer = document.createElement("div", (id = "similarity-score"));
  simcontainer.innerHTML = `
      <h1>Similarity Score: ${similarityScore.similarity_score}</h1>
      <div id="bar">
        <div id="true">${similarityScore.similarity_score}%</div>
        <div id="false">${100 - similarityScore.similarity_score}%</div>
      </div>
      <style>
        #bar {
            display : flex;
            height : 20px;
            width : 100%;
        }
        #true {
            justify-self: left;
            height: 20px;
            width: ${similarityScore.similarity_score}%;
            background-color: green;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            text-align: center;
        }
        #false {
            justify-self : right;
            height: 20px;
            width: ${100 - similarityScore.similarity_score}%;
            background-color: red;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            text-align: center;
        }
      </style>
      <p>${similarityScore.reasoning}</p>`;
  return simcontainer;
};

const formatFactCheck = (factCheck) => {
  return `
        <li>
            <h3 class="llm-claim">\"${factCheck.llm_claim}\"</h3>
            <p class="check">${factCheck.check}</p>
            <p><a href="${factCheck.backup.link}" target="_blank">Source: \"${factCheck.backup.quote}\"</a></p>
        </li>
    `;
};

const formatFactChecks = (factChecks) => {
  factcontainer = document.createElement("div", (id = "fact-checks"));
  factcontainer.innerHTML = `
        <h1>Fact Checks</h1>
        <ul>
            ${factChecks
              .map((factCheck) => formatFactCheck(factCheck))
              .join("")}
        </ul>
    `;
  return factcontainer;
};
