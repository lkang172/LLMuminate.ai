function start() {
  var output = document.createElement("p");
  output.id = "#message";
  var title = document.querySelector("#title");

  chrome.tabs
    .query({ active: true, currentWindow: true })
    .then(function (tabs) {
      var activeTab = tabs[0];
      var activeTabId = activeTab.id;

      return chrome.scripting.executeScript({
        target: { tabId: activeTabId },
        func: DOMtoString,
      });
    })
    .then(function (results) {
      var html = results[0].result;
      var parser = new DOMParser();
      var doc = parser.parseFromString(html, "text/html");
      if (
        doc
          .querySelector("meta[property='og:title']")
          .getAttribute("content") == "ChatGPT"
      ) {
        var convo = [];
        var i = 2;
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
        document.body = factCheck(convo[convo.length - 1]);
      } else if (
        doc.querySelector("title").textContent.search("Claude") != -1
      ) {
        document.body = factCheck(
          doc
            .querySelector('div[data-test-render-count="1"]')
            .getElementsByClassName("font-claude-message")[0].textContent
        );
      } else if (
        doc
          .querySelector("meta[property='og:site_name']")
          .getAttribute("content") == "Gemini"
      ) {
        var responses = doc.querySelectorAll("message-content");
        document.body = factCheck(responses[responses.length - 1].textContent);
      } else {
        throw new Error("");
      }
    })
    .catch(function (error) {
      const textInput = document.createElement("textarea");
      textInput.id = "text-input";
      textInput.className = "scrollable-box";
      const button = document.createElement("button");
      button.textContent = "Submit";
      button.id = "submit";
      button.className = "center";
      button.addEventListener("click", () => {
        document.body.removeChild(textInput);
        document.body.removeChild(button);
        document.body = factCheck(textInput.value);
      });
      document.body.appendChild(textInput);
      document.body.appendChild(button);
      title.innerText =
        "No prompt from Claude, Gemini, or ChatGPT detected. Please enter the information you want to fact check.";
      // title.innerText = error
    });
}
alreadyStarted = false;
if (!alreadyStarted) window.onload = start;

function DOMtoString(selector) {
  if (selector) {
    selector = document.querySelector(selector);
    if (!selector) return "ERROR: querySelector failed to find node";
  } else {
    selector = document.documentElement;
  }
  return selector.outerHTML;
}

function factCheck(input) {
  const apiUrl = "";

  // const requestOptions = {
  //     method : 'POST',
  //     body : {"message" : input}
  // }

  // fetch(apiUrl, requestOptions)
  //   .then(response => {
  //     if (!response.ok) {
  //       throw new Error('Network response was not ok');
  //     }
  //     return response.json();
  //   })
  //   .then(data => {
  //     container = document.createElement("div", className="container")
  //     container.appendChild(formatSimilarityScore(data.similarityAssessment))
  //     container.appendChild(formatFactChecks(data.factChecks))
  //   })
  //   .catch(error => {
  //     console.error('Error:', error);
  //   });
  data = {
    fact_checks: [
      {
        llm_claim:
          "COVID-19 can lead to dehydration, so maintaining fluid intake is crucial",
        check:
          "The articles don't specifically address hydration, but discuss general supportive therapy",
        backup: {
          quote:
            "The current management of COVID-19 is based generally on supportive therapy and treatment to prevent respiratory failure",
          link: "https://pubmed.ncbi.nlm.nih.gov/32749914/",
        },
      },
      {
        llm_claim:
          "If symptoms worsen (e.g., difficulty breathing, chest pain, confusion), seek medical attention immediately",
        check:
          "This claim is supported by the literature, which identifies these as serious symptoms",
        backup: {
          quote:
            "Manifestations of COVID-19 include asymptomatic carriers and fulminant disease characterized by sepsis and acute respiratory failure. Approximately 5% of patients with COVID-19, and 20% of those hospitalized, experience severe symptoms necessitating intensive care",
          link: "https://pubmed.ncbi.nlm.nih.gov/32648899/",
        },
      },
      {
        llm_claim: "COVID-19 isolation can lead to anxiety or loneliness",
        check:
          "Multiple studies confirm the mental health impact of COVID-19 isolation",
        backup: {
          quote:
            "The COVID-19 pandemic's physical restrictions and social distancing measures have affected each and every domain of life... Anxiety, depression, disturbances in sleep and appetite, as well as impairment in social interactions are the most common presentations",
          link: "https://pubmed.ncbi.nlm.nih.gov/33810225/",
        },
      },
    ],
    similarity_assessment: {
      reasoning:
        "The AI response generally aligns with scientific literature regarding COVID-19 management and symptoms. It accurately reflects the importance of monitoring symptoms, seeking medical attention when needed, and acknowledging both physical and mental health impacts. However, some specific recommendations (like hydration and specific medications) aren't directly addressed in the provided articles. The response takes a more practical, patient-focused approach while maintaining accuracy with available scientific evidence.",
      similarity_score: 80,
    },
  };
  container = document.createElement("body");
  container.appendChild(formatSimilarityScore(data.similarity_assessment));
  container.appendChild(formatFactChecks(data.fact_checks));

  // const resetButton = document.createElement("button");
  // resetButton.textContent = "Reset";
  // resetButton.className = "center"; // Apply the 'center' class
  // resetButton.style.margin = "10px auto"; // Center the button using margin
  // resetButton.addEventListener('click', start);
  // container.appendChild(resetButton);
  // alreadyStarted = true
  return container;
}

function formatSimilarityScore(similarityScore) {
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
            justify-self : left;
            height : 20px;
            width : ${similarityScore.similarity_score}%;
            background-color : green;
            border-top-left-radius : 10px;
            border-bottom-left-radius : 10px;
            text-align : center;
        }
        #false {
            justify-self : right;
            height : 20px;
            width : ${100 - similarityScore.similarity_score}%;
            background-color : red;
            border-top-right-radius : 10px;
            border-bottom-right-radius : 10px;
            text-align : center;
        }
      </style>
      <p>${similarityScore.reasoning}</p>`;

  return simcontainer;
}

function formatFactCheck(factCheck) {
  return `
        <li>
            <h3 class="llm-claim">\"${factCheck.llm_claim}\"</h3>
            <p class="check">${factCheck.check}</p>
            <p><a href="${factCheck.backup.link}" target="_blank">Sourc: \"${factCheck.backup.quote}\"</a></p>
        </li>
    `;
}

function formatFactChecks(factChecks) {
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
}
