## Summarization, Risk Analysis, Action Items

```mermaid
flowchart LR
  A((Start))-->B([Add text to<br/>be analyzed as context])
  B-->O([Prompt<br/>OpenAI API])
  classDef blue fill:blue,color:#fefefe
  class A,B,O blue
```

Jupyter notebook:

- [Analysis](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/analysis.ipynb)

Examples:

```python
contract = mock_get_contract("LEASE_AGREEMENT")
prompt = f'Summarize and list risks.\n[context]\n{contract}'
```

- Sample 1:

  > Prompt:<br/>Summarize and list risks.<br/><br/>Content:<br/>RESIDENTIAL LEASE AGREEMENT<br/>
  > RENT. The Tenant shall pay to Landlord the sum of $1,500 per month (hereinafter referred to as "Rent") for the duration of the Term of the Lease. The Rent shall be payable on or before every day of the month (hereinafter referred to as the "Due Date"), notwithstanding that the said date falls on a weekend or holiday.<br/>
  > A. Late Rent. If Rent is not paid within days of the Due Date, the Rent shall be considered past due, and a late fee of a $50 or 5% of the Rent past due shall be applied for every day Rent is late or O occurrence Rent is late.<br/>B. Returned Checks. In the event that a check intended as payment for Rent is dishonored for whatever reason, the same shall be considered as Late Rent with the late fee being payable on the same.<br/><br/>Completion:<br/>Summary:<br/>The residential lease agreement states that the tenant must pay $1,500 per month on or before the due date, with a late fee of $50 or 5% of the rent past due if payment is not made within days of the due date. If a check intended as payment is dishonored, it will also be considered as late rent with the late fee being payable on the same.<br/>Risks:<br/>- Risk of incurring late fees if rent is not paid on time.<br/>- Risk of incurring additional fees if a check intended as payment is dishonored.<br/>- Risk of potential legal action if rent is consistently paid late or not at all.

- Sample 2:
  > Prompt:<br/>What is my best investment?<br/><br/>Context:<br/>Portfolio:<br/>- 100 shares of MSFT at $100. Today's price is $295.<br/>- 100 shares of TSLA at $1000. Today's price is $153.<br/><br/>Completion:<br/>Based on the current prices, your best investment would be the 100 shares of MSFT that you own. The value of your MSFT shares has increased significantly since you purchased them, and they are now worth $29,500 (100 shares x $295 per share), compared to the $10,000 you originally invested. On the other hand, your TSLA shares have decreased in value and are now worth $15,300 (100 shares x $153 per share), which is a loss of $84,700 from your original investment of $100,000. However, it's important to note that past performance is not a guarantee of future results, and it's always a good idea to do your own research and consult with a financial advisor before making any investment decisions.
