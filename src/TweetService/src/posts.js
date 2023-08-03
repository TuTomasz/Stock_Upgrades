window.onload = function () {
  async function getData() {
    const response = await fetch(
      "https://raw.githubusercontent.com/TuTomasz/Stock_Upgrades/main/Data/Queue/Insight.json"
    );
    const data = await response.json();

    console.log(data);
    return data;
  }

  function buildHtml(data) {
    let html = "";
    let template = `<div id="ID"class="Tweet"}>
            <h3> $TICKER - COMPANY </h3>
            
            <div class="Rating">
                <div class="Box">
                <div id="Text">Analyst Score</div>
                <div id="Score">SCORE</div>
                </div>
                <div class="Box">
                <div id="Text">Price Target</div>
                <div id="Score">PRICETARGET</div>
                </div>
                <div class="Box">
                <div id="Text">Number of Analysts</div>
                <div id="Score">ANALYSTS</div>
                </div>
                <div class="Box">
                <div id="Text">Period</div>
                <div id="Score">180 days</div>
                </div>
                <div class="Box">
                <div id="Text">Sentiment</div>
                <div id="Score">RATING</div>
                </div>
            </div>
            <div class="Disclamer">
                For informational purposes only, not intended as investment advice
            </div>
        </div>`;

    for (const [ticker, insight] of Object.entries(data)) {
      console.log(`${ticker}: ${insight.Company}`);

      let newTemplate = template;
      let priceTarget = "$" + insight.Price_Target;

      newTemplate = newTemplate.replace("ID", ticker);
      newTemplate = newTemplate.replace("TICKER", ticker);
      newTemplate = newTemplate.replace("COMPANY", insight.Company);
      newTemplate = newTemplate.replace("SCORE", insight.Letter_Rating);
      newTemplate = newTemplate.replace("PRICETARGET", priceTarget);
      newTemplate = newTemplate.replace("ANALYSTS", insight.Number_of_Analysts);
      newTemplate = newTemplate.replace("RATING", insight.Cumulative_Rating);

      html += newTemplate;
    }

    return html;
  }
  (() => {
    getData().then((data) => {
      let html = buildHtml(data);
      document.getElementsByClassName("Container")[0].innerHTML = html;
    });
  })();
};
