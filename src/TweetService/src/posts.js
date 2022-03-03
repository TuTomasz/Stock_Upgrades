window.onload = function () {
  console.log("loaded");

  async function getData() {
    const response = await fetch(
      "https://raw.githubusercontent.com/TuTomasz/Stock_Upgrades/main/Data/Queue/Insight.json"
    );
    const data = await response.json();
    return data;
  }

  function buildHtml(data) {
    console.log("test");
    console.log(data);
    console.log(data.length);
    var size = Object.keys(data).length;

    let html = "";

    let template = `<div id="ID"class="Tweet"}>
            <h3> $TICKER - COMPANY </h3>
            
            <div class="Rating">
                <div class="Box">
                <div id="ScoreText">Score</div>
                <div id="Score">SCORE</div>
                </div>
                <div class="Box">
                <div id="ScoreText">Price Target</div>
                <div id="Score">PRICETARGET</div>
                </div>
                <div class="Box">
                <div id="ScoreText">Number of Analysts</div>
                <div id="Score">ANALYSTS</div>
                </div>
                <div class="Box">
                <div id="ScoreText">Sentiment</div>
                <div id="Score">RATING</div>
                </div>
            </div>
            <div class="Disclamer">
                For informational purposes only, not intended as investment advice
            </div>
        </div>`;

    // iterate over object values ou data object
    for (const [ticker, insight] of Object.entries(data)) {
      console.log(`${ticker}: ${insight.Company}`);
      let newTemplate = template;
      let priceTarget = "$" + insight.Price_Target;

      newTemplate = newTemplate.replace("ID", ticker);
      newTemplate = newTemplate.replace("TICKER", ticker);
      newTemplate = newTemplate.replace("COMPANY", insight.Company);
      newTemplate = newTemplate.replace("SCORE", insight.Score);
      newTemplate = newTemplate.replace("PRICETARGET", priceTarget);
      newTemplate = newTemplate.replace("ANALYSTS", insight.Number_of_Analysts);
      newTemplate = newTemplate.replace("RATING", insight.Cumulative_Rating);

      html += newTemplate;
    }

    return html;

  }

  // self invoking main function
  (() => {
    getData().then((data) => {
     let html = buildHtml(data);
      document.getElementsByClassName("Container")[0].innerHTML = html;
    });
  })();



};
