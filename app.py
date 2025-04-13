from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__)
CORS(app)  # Allow frontend access from any origin

@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    data = request.get_json()
    ticker = data.get("ticker", "").upper()
    growth = float(data.get("growth_rate", 10)) / 100
    discount = float(data.get("discount_rate", 8)) / 100
    terminal = float(data.get("terminal_growth_rate", 2)) / 100
    years = int(data.get("years", 5))

    try:
        stock = yf.Ticker(ticker)
        cashflows = stock.cashflow

        # Safely get Free Cash Flow (or fallback)
        try:
            fcf = cashflows.loc['Total Cash From Operating Activities'].iloc[-1]
            fcf = float(fcf)
        except Exception:
            fcf = 5_000_000_000  # Fallback value

        # Simple DCF calculation
        dcf_value = 0
        for year in range(1, years + 1):
            projected_fcf = fcf * ((1 + growth) ** year)
            dcf_value += projected_fcf / ((1 + discount) ** year)

        terminal_value = (fcf * (1 + terminal)) / (discount - terminal)
        terminal_value /= ((1 + discount) ** years)
        total_value = dcf_value + terminal_value

        # AI-style mock insights
        response = {
            "problem_it_solves": "Helps enterprises manage large-scale cloud and AI infrastructure efficiently.",
            "customer_base_size": "Thousands of enterprise clients, including major hyperscalers.",
            "moat_strength": "Unified software stack, high switching costs, and strong hyperscaler partnerships.",
            "operational_efficiency": "Gross margin ~60%, operating margin ~38%. Asset-light model.",
            "dcf_valuation": f"${total_value:,.2f}",
            "ai_opportunities": "Positioned to power next-gen AI data centers with high-throughput, low-latency networking fabrics."
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Bind to 0.0.0.0 and use Render-provided PORT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)